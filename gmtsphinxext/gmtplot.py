# pylint: disable=exec-used
"""
Sphinx extension for including live rendered GMT plots within sphinx documentation.
"""
import io
import os
import sys
import ast
import warnings
import contextlib
import base64
import tempfile
import subprocess

import jinja2

from IPython.display import Image, HTML

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives import flag, unchanged

from sphinx.locale import _


HTML_TEMPLATE = jinja2.Template(
    """
<div class="gmtplot-output" id="{{ div_id }}">
    {% if stdout %}
        <div class="highlight">
            <pre>{{ stdout }}</pre>
        </div>
    {% endif %}
    {% if image or html %}
        {% set center_style="display: block; margin-left: auto; margin-right: auto;" %}
        <div class="gmtplot-output-figure">
            {% if image %}
                <img src="data:image/png;base64,{{ image }}"
                     style="{% if width %}width: {{ width }};{% endif %}
                            {% if center %}{{ center_style }}{% endif %}">
            {% endif %}
            {% if html %}
                {{ html }}
            {% endif %}
        </div>
    {% endif %}
</div>
"""
)


class GMTPlotNode(nodes.General, nodes.Element):
    """
    Sphinx node for a GMT plot.
    """

    pass


class GMTPlotDirective(Directive):
    """
    The gmt-plot directive implementation. This is what defines what the directive does
    and how to build the rst document tree from the directive content.
    """

    has_content = True

    option_spec = {
        "language": unchanged,
        "figure": unchanged,
        "hide-code": flag,
        "namespace": unchanged,
        "alt": unchanged,
        "width": unchanged,
        "center": flag,
    }

    def run(self):
        """
        Build the rst document node from the directive content.
        """
        env = self.state.document.settings.env

        if not hasattr(env, "gmt_namespaces"):
            env.gmt_namespaces = {}
        namespace = env.gmt_namespaces.setdefault(env.docname, {}).setdefault(
            self.options.get("namespace", "default"), {}
        )

        code = "\n".join(self.content)

        # Get the name of the source file we are currently processing
        rst_source = self.state_machine.document["source"]
        rst_dir = os.path.dirname(rst_source)
        rst_filename = os.path.basename(rst_source)

        # Use the source file name to construct a friendly target_id
        rst_base = rst_filename.replace(".", "-")
        serialno = env.new_serialno("gmt-plot")
        div_id = "{0}-gmt-plot-{1}".format(rst_base, serialno)
        target_id = "{0}-gmt-source-{1}".format(rst_base, serialno)

        # Create the node in which the plot will appear. This will be processed by
        # html_visit_gmt_plot
        plot_node = GMTPlotNode()
        plot_node["target_id"] = target_id
        plot_node["div_id"] = div_id
        plot_node["code"] = code
        plot_node["namespace"] = namespace
        plot_node["relpath"] = os.path.relpath(rst_dir, env.srcdir)
        plot_node["rst_source"] = rst_source
        plot_node["rst_lineno"] = self.lineno
        plot_node["language"] = self.options.get("language", "bash")
        plot_node["figure"] = self.options.get("figure", "")
        plot_node["width"] = self.options.get("width", "")
        plot_node["center"] = "center" in self.options
        if "alt" in self.options:
            plot_node["alt"] = self.options["alt"]

        result = [nodes.target("", "", ids=[target_id])]
        if "hide-code" not in self.options:
            source_literal = nodes.literal_block(code, code)
            source_literal["language"] = plot_node["language"]
            result.append(source_literal)
        result.append(plot_node)
        return result


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


def eval_python(code, namespace=None, filename="<string>"):
    """
    Execute a multi-line block of Python code in the given namespace.

    If the final statement in the code is an expression, return the result of the
    expression.
    """
    tree = ast.parse(code, filename="<ast>", mode="exec")
    if namespace is None:
        namespace = {}
    if isinstance(tree.body[-1], ast.Expr):
        to_exec, to_eval = tree.body[:-1], tree.body[-1:]
    else:
        to_exec, to_eval = tree.body, []
    for node in to_exec:
        compiled = compile(ast.Module([node]), filename=filename, mode="exec")
        exec(compiled, namespace)
    catch_display = _CatchDisplay()
    with catch_display:
        for node in to_eval:
            compiled = compile(
                ast.Interactive([node]), filename=filename, mode="single"
            )
            exec(compiled, namespace)
    return catch_display.output


def eval_bash(code, figure):
    """
    Execute a multi-line block of bash code and load the specified image file.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        script = os.path.join(tmpdir, "script.sh")
        with open(script, "w") as fout:
            fout.write(code)
        proc = subprocess.run(
            "bash {}".format(script),
            shell=True,
            cwd=tmpdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if proc.returncode != 0:
            raise RuntimeError(
                "GMT bash failed:\nSTDOUT: {}\nSTDERR: {}".format(
                    proc.stdout.decode("utf-8"), proc.stderr.decode("utf-8")
                )
            )
        figure = os.path.join(tmpdir, figure)
        with open(figure, "rb") as fin:
            image = fin.read()
    return image


def html_visit_gmt_plot(self, node):
    """
    Execute the code and produce output for HTML.
    """
    # Execute the code, saving output and namespace
    namespace = node["namespace"]
    try:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            if node["language"] == "python":
                returned = eval_python(node["code"], namespace)
            if node["language"] == "bash":
                returned = eval_bash(node["code"], node["figure"])
            else:
                raise ValueError("Invalid language '{}'".format(node["language"]))
        stdout = output.getvalue()
    except Exception as e:
        warnings.warn(
            "gmt-plot: {0}:{1} Code execution failed with: {2}: {3}".format(
                node["rst_source"], node["rst_lineno"], e.__class__.__name__, str(e)
            )
        )
        raise e

    if stdout or returned is not None:
        image = ""
        html = ""
        if isinstance(returned, Image):
            image = base64.encodebytes(returned.data).decode("utf-8")
        elif isinstance(returned, HTML):
            html = returned.data
        else:
            # Assume it's a PNG loaded as bytes
            image = base64.encodebytes(returned).decode("utf-8")
        self.body.append(
            HTML_TEMPLATE.render(
                div_id=node["div_id"],
                stdout=stdout,
                html=html,
                image=image,
                width=node["width"],
                center=node["center"],
            )
        )
    # Always skip the node because we're inserting things directly into the HTML body
    raise nodes.SkipNode


def generic_visit_gmt_plot(self, node):  # pylint: disable=unused-argument
    """
    Execute code and generate output for other formats.
    """
    # Should generate PNGs and insert them here
    self.body.append(_("[ GMT Figure ]"))
    raise nodes.SkipNode


def depart_gmt_plot(self, node):  # pylint: disable=unused-argument
    """
    Actions to take at the end of a plot directive.
    """
    return None


def purge_namespaces(app, env, docname):  # pylint: disable=unused-argument
    """
    Clean up the execution namespace.
    """
    if not hasattr(env, "gmt_namespaces"):
        return
    env.gmt_namespaces.pop(docname, {})


def setup(app):
    """
    Add the directive to the sphinx app.
    """
    setup.app = app
    setup.config = app.config
    setup.confdir = app.confdir
    app.add_directive("gmt-plot", GMTPlotDirective)
    app.add_node(
        GMTPlotNode,
        html=(html_visit_gmt_plot, depart_gmt_plot),
        latex=(generic_visit_gmt_plot, depart_gmt_plot),
        texinfo=(generic_visit_gmt_plot, depart_gmt_plot),
        text=(generic_visit_gmt_plot, depart_gmt_plot),
        man=(generic_visit_gmt_plot, depart_gmt_plot),
    )
    app.connect("env-purge-doc", purge_namespaces)
    return {"version": "0.1"}
