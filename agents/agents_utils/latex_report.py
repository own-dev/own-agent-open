"""
LaTeX report generation utils functionality module
"""
import os
import traceback
from typing import Optional, Dict

from data import Data
from jinja2.loaders import FileSystemLoader
from latex import escape, build_pdf
from latex.jinja2 import make_env

import utils.logger as logger
from agents.agents_utils.utils_constants import AGENT_UTILS_NAME

TEX_DEFAULT_PLACEHOLDER = ''


def read_and_fill_template(template_filepath: str, data: Optional[Dict] = None) -> Optional[str]:
    """
    Builds the given template with the given data

    :param template_filepath: Path of the template to use
    :param data: Keywords-values for the given LaTeX-template

    :return: built LaTeX-report path if it was compiled, otherwise None
    """
    # Make up the environment
    split_template_path = template_filepath.split('/')
    latex_templates_dir_path = '/'.join(split_template_path[:-1])
    latex_template_path = split_template_path[-1]
    env = make_env(loader=FileSystemLoader(searchpath=latex_templates_dir_path), autoescape=False)

    # Get the template
    if not os.path.exists(template_filepath):
        logger.error(AGENT_UTILS_NAME, f'No template is found: {template_filepath}')
        return None
    template = env.get_template(latex_template_path)

    # Put the data into the template and render the text
    try:
        rendered_template = template.render(**data)
    except Exception as e:
        rendered_template = None
        logger.error(AGENT_UTILS_NAME, f'Can\'t render LaTeX template. Message: {e}')

    return rendered_template


def build_report(template_filepath: str, data: Optional[Dict] = None,
                 builder: Optional[str] = None) -> Optional[Data]:
    """
    Builds the given template with the given data

    :param template_filepath: Template's path to use
    :param data: Keywords-values for the given LaTeX-template
    :param builder: Builder to use 'latexmk', 'pdflatex', 'xelatexmk'; None = default = 'pdflatex

    :return: LaTeX-report
    """
    # Put the data into the template
    rendered_template = read_and_fill_template(template_filepath, data)
    if not rendered_template:
        logger.error(AGENT_UTILS_NAME, f'Template was not found or filled correctly: {template_filepath}')
        return None

    # Build the template, and save the result to a file
    try:
        pdf = build_pdf(rendered_template, builder=builder)
    except Exception as e:
        pdf = None
        tb = traceback.format_exc()
        logger.error(AGENT_UTILS_NAME, f'Cant build LaTeX report with builder "{builder}" and data: "{data}".\n'
                                       f'Message: {e}.\nStackTrace: {tb}')

    return pdf


def characters_escaper(text: str) -> str:
    """
    LaTeX characters escaper
    :param text: Text to escape
    :return: Escaped string or default placeholder..
    """
    return escape(text) if isinstance(text, str) else TEX_DEFAULT_PLACEHOLDER
