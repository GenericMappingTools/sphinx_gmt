"""
A directive for including a GMT plot in a Sphinx document.

Options
-------

The ``gmtplot`` directive supports the following options:

    show-code : bool
        Whether to display the source code. The default can be changed using the
        ``gmtplot_show_code`` variable in ``conf.py``.

    language : {'python', 'bash'}
        Specify the language of the source code. The default can be changed using the
        `highlight_language` variable in conf.py.

    caption : str
        Caption of the rendered figure.

Additionally, this directive supports options of the ``figure`` and ``literalinclude``
directives.

Configuration options
---------------------

The following options can be set in ``conf.py`` and will apply globally:

    gmtplot_show_code : bool
        Default value for the ``show-code`` option.

    gmtplot_basedir : str
        Base directory, to which ``gmtplot`` file names are relative to. If None or
        empty, file names are relative to the directory where the file containing the
        directive is. However, if it is absolute (starting with ``/``), it is relative
        to the top source directory.

"""

import os
import sys
import ast
import shutil
import tempfile
import subprocess
import textwrap
from pathlib import Path

from docutils.parsers.rst import Directive, directives
import jinja2


TEMPLATE = """
{%- if show_code -%}
.. literalinclude:: {{ code }}
    {% for option in code_opts -%}
    {{ option }}
    {% endfor %}
{%- else %}
:download:`Source Code <{{ code }}>`
{%- endif %}

.. figure:: {{ image }}
    {% for option in image_opts -%}
    {{ option }}
    {% endfor %}

    {{ caption }}

"""


def _option_language(arg):
    """Check language option."""
    return directives.choice(arg, ("bash", "python"))


def _option_boolean(arg):
    # pylint: disable=no-else-return
    """Check boolean options."""
    if not arg or not arg.strip():  # no argument given, assume used as a flag
        return True
    elif arg.strip().lower() in ("no", "0", "false"):
        return False
    elif arg.strip().lower() in ("yes", "1", "true"):
        return True
    else:
        raise ValueError('"{}" unknown boolean'.format(arg))


def _option_align(arg):
    """Check align option."""
    return directives.choice(
        arg, ("top", "middle", "bottom", "left", "center", "right")
    )


def _set_gmt_datadir(cwd):
    """Set evirionment variable GMT_DATADIR so that script can access
    its data files.

    Retures
    =======

    old_gmt_datadir : str
        Previous value of GMT_DATADIR.
    """
    old_gmt_datadir = os.environ.get("GMT_DATADIR")
    if old_gmt_datadir:
        sep = ";" if sys.platform == "win32" else ":"
        os.environ["GMT_DATADIR"] = str(cwd) + sep + os.environ["GMT_DATADIR"]
    else:
        os.environ["GMT_DATADIR"] = str(cwd)
    return old_gmt_datadir


def _reset_gmt_datadir(old_gmt_datadir):
    """Reset environment variable GMT_DATADIR to its old value."""
    if old_gmt_datadir:
        os.environ["GMT_DATADIR"] = old_gmt_datadir
    else:
        del os.environ["GMT_DATADIR"]


def _search_images(cwd):
    # pylint: disable=no-else-return,no-else-raise
    """
    Search images in PNG and PDF format in a specified directory.
    If .png and .pdf files are not found and .ps file is found, then
    convert .ps file to PNG and PDF format.
    """
    cwd = Path(cwd)
    png_images = list(cwd.glob("*.png"))

    if len(png_images) > 1:
        raise ValueError("More than one figure generated in one GMT plot.")
    elif len(png_images) == 1:
        pdf_images = list(cwd.glob("*.pdf"))
        if len(pdf_images) == 1:
            return [png_images[0], pdf_images[0]]
        else:
            return [png_images[0]]
    else:  # no PNG found
        ps_images = list(cwd.glob("*.ps"))
        if len(ps_images) > 1:
            raise ValueError("More than one figure generated in one GMT plot.")
        elif len(ps_images) == 1:  # PS found
            cmd = "gmt psconvert -A -P -T{} {}"
            subprocess.run(cmd.format("g", ps_images[0]), shell=True)
            subprocess.run(cmd.format("f", ps_images[0]), shell=True)
            png_images = list(cwd.glob("*.png"))
            pdf_images = list(cwd.glob("*.pdf"))

            if len(png_images) == 1 and len(pdf_images) == 1:
                return [png_images[0], pdf_images[0]]
            else:
                return []
        else:  # No PNG and PS found
            return []


def eval_bash(code, code_dir, output_dir, output_base):
    """
    Execute a multi-line block of bash code and copy the generated image files
    to specified output directory.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        Path(tmpdir, "script.sh").write_text(code, encoding="utf-8")

        old_gmt_datadir = _set_gmt_datadir(code_dir)
        proc = subprocess.run(
            "bash {}".format(Path(tmpdir, "script.sh")),
            shell=True,
            cwd=tmpdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        _reset_gmt_datadir(old_gmt_datadir)
        if proc.returncode != 0:
            raise RuntimeError(
                "GMT bash failed:\nSTDOUT: {}\nSTDERR: {}".format(
                    proc.stdout.decode("utf-8"), proc.stderr.decode("utf-8")
                )
            )
        for image in _search_images(tmpdir):
            shutil.move(image, Path(output_dir, output_base).with_suffix(image.suffix))
        return output_base + ".*"


class _CatchDisplay:  # pylint: disable=too-few-public-methods
    "Class to temporarily catch sys.displayhook"

    def __init__(self):
        self.output = None

    def __enter__(self):
        self.old_hook = sys.displayhook
        sys.displayhook = self
        return self

    def __exit__(self, dtype, value, traceback):
        sys.displayhook = self.old_hook
        # Returning False will cause exceptions to propagate
        return False

    def __call__(self, output):
        self.output = output


def eval_python(code, code_dir, output_dir, output_base, filename="<string>"):
    # pylint: disable=exec-used
    """
    Execute a multi-line block of Python code and copy the generated image files
    to specified output directory.
    """
    tree = ast.parse(code, filename="<ast>", mode="exec")
    if (
        isinstance(tree.body[-1], ast.Expr) and tree.body[-1].value.func.attr == "show"
    ):  # last statement is `fig.show()` in pygmt
        to_exec, to_eval = tree.body[:-1], tree.body[-1:]
    else:
        to_exec, to_eval = tree.body, []

    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        old_gmt_datadir = _set_gmt_datadir(code_dir)

        for node in to_exec:
            exec(compile(ast.Module([node]), filename=filename, mode="exec"))
        _reset_gmt_datadir(old_gmt_datadir)

        images = _search_images(tmpdir)
        if images:
            for image in images:
                shutil.move(
                    image, Path(output_dir, output_base).with_suffix(image.suffix)
                )
        else:
            catch_display = _CatchDisplay()
            with catch_display:
                for node in to_eval:
                    exec(
                        compile(
                            ast.Interactive([node]), filename=filename, mode="single"
                        )
                    )
            Path(output_dir, output_base).with_suffix(".png").write_bytes(
                catch_display.output.data
            )
    os.chdir(cwd)
    return output_base + ".*"


def render_figure(code, code_dir, language, output_dir, output_base):
    """
    Run a GMT code and save the images in *output_dir* with file names
    derived from *output_base*.
    """
    if language == "bash":
        figname = eval_bash(code, code_dir, output_dir, output_base)
    elif language == "python":
        figname = eval_python(code, code_dir, output_dir, output_base)
    return figname


def guess_language(filename):
    # pylint: disable=no-else-return
    """Guess language from suffix of the script."""
    suffix = Path(filename).suffix
    if suffix in [".sh", ".bash"]:
        return "bash"
    elif suffix == ".py":
        return "python"
    else:
        raise ValueError("Cannot guess language from {}".format(filename))


def get_suffix_from_language(language):
    """Determine suffix from language."""
    if language == "bash":
        suffix = "sh"
    elif language == "python":
        suffix = "py"
    return suffix


class GMTPlotDirective(Directive):
    """
    The gmtplot directive implementation.
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False

    # options list of literalinclude directive
    options_code = {
        "dedent": int,
        "linenos": directives.flag,
        "lineno-start": int,
        "lineno-match": directives.flag,
        "tab-width": int,
        "language": _option_language,
        "encoding": directives.encoding,
        "lines": directives.unchanged_required,
        "start-after": directives.unchanged_required,
        "end-before": directives.unchanged_required,
        "start-at": directives.unchanged_required,
        "end-at": directives.unchanged_required,
        "prepend": directives.unchanged_required,
        "append": directives.unchanged_required,
        "emphasize-lines": directives.unchanged_required,
        "name": directives.unchanged,
    }
    # options list of figure directive
    options_figure = {
        "alt": directives.unchanged,
        "height": directives.length_or_unitless,
        "width": directives.length_or_percentage_or_unitless,
        "scale": directives.nonnegative_int,
        "align": _option_align,
        "class": directives.class_option,
    }
    option_spec = {
        "show-code": _option_boolean,
        "caption": directives.unchanged,
        **options_code,
        **options_figure,
    }

    def run(self):
        # pylint: disable=too-many-locals
        document = self.state_machine.document
        env = self.state_machine.document.settings.env
        config = self.state_machine.document.settings.env.config

        # set options to default values if not specified
        self.options.setdefault("show-code", config.gmtplot_show_code)
        self.options.setdefault("align", config.gmtplot_figure_align)

        # Get the name of the rst source file we are currently processing
        rst_file = Path(document["source"])

        # current working directory of the rst source file
        cwd = rst_file.parent

        counter = env.new_serialno("gmtplot")
        output_base = "{}-gmtplot-{}".format(rst_file.stem, counter)
        caption = ""

        if self.arguments:  # load codes from a file
            # Guess language from suffix of the script
            if "language" not in self.options:
                self.options["language"] = guess_language(self.arguments[0])

            # Get absolute path of the script
            if config.gmtplot_basedir:  # relative to gmtplot_basedir
                code_file = Path(
                    env.app.srcdir, config.gmtplot_basedir, self.arguments[0]
                )
            elif self.arguments[0].startswith("/"):  # relative to source directory
                code_file = Path(env.app.srcdir, self.arguments[0][1:])
            else:  # relative to current rst file's path
                code_file = Path(cwd, self.arguments[0])
            code_file = code_file.absolute()
            code_basedir = code_file.parent
            code = code_file.read_text(encoding="utf-8")

            # If there is content, it will be passed as a caption.
            caption = "\n".join(self.content)
        else:  # inline codes
            self.options.setdefault("language", config.highlight_language)
            code_basedir = cwd
            code = textwrap.dedent("\n".join(map(str, self.content)))
            if "caption" in self.options:
                caption = self.options["caption"]

        # determine unique code filename under current working directory
        suffix = get_suffix_from_language(self.options["language"])
        code_file = Path(cwd, "{}.{}".format(output_base, suffix))

        if self.options["show-code"]:
            code_opts = []
            for key, val in self.options.items():
                if key == "linenos":
                    code_opts.append(":{}:".format(key))
                elif key in self.options_code.keys():
                    code_opts.append(":{}: {}".format(key, val))
        else:
            code_opts = ""

        image_opts = [
            ":{}: {}".format(key, val)
            for key, val in self.options.items()
            if key in self.options_figure.keys()
        ]

        # builddir: where to place output files (temporarily)
        builddir = (
            Path(env.app.doctreedir).parent
            / "gmtplot_directive"
            / cwd.relative_to(env.app.srcdir)
        )
        # determine how to link to files in builddir from the RST file
        # use os.path.relpath rather than relative_to!
        builddir_link = Path("/", os.path.relpath(str(builddir), env.app.srcdir))

        # copy script to builddir
        builddir.mkdir(parents=True, exist_ok=True)
        Path(builddir, code_file.name).write_text(code, encoding="utf-8")

        # make figures
        image = render_figure(
            code, code_basedir, self.options["language"], builddir, output_base
        )

        gmtplot_block = (
            jinja2.Template(TEMPLATE)
            .render(
                show_code=self.options["show-code"],
                code=builddir_link / code_file.name,
                code_opts=code_opts,
                image=builddir_link / image,
                image_opts=image_opts,
                caption=caption,
            )
            .split("\n")
        )
        gmtplot_block.extend("\n")
        self.state_machine.insert_input(gmtplot_block, source=str(rst_file))

        return []


def setup(app):
    """
    Add the gmtplot directive to the sphinx app.
    """
    setup.app = app
    setup.config = app.config
    setup.confdir = app.confdir

    app.add_directive("gmtplot", GMTPlotDirective)
    app.add_config_value("gmtplot_basedir", None, True)
    app.add_config_value("gmtplot_show_code", True, True)
    app.add_config_value("gmtplot_figure_align", "center", True)
    metadata = {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
    return metadata
