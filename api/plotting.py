"""Plot rendering module - generates base64 PNG images from plot data."""

import base64
import io
from typing import TYPE_CHECKING

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server-side rendering
import matplotlib.pyplot as plt
import numpy as np

if TYPE_CHECKING:
    from mathlang.types.result import PlotData2D, PlotData3D, HistogramData, ScatterData

# Dark theme colors matching the web UI
DARK_THEME = {
    'bg_color': '#1f2937',      # gray-800
    'plot_bg': '#111827',        # gray-900
    'text_color': '#e5e7eb',     # gray-200
    'grid_color': '#374151',     # gray-700
    'line_color': '#10b981',     # green-500
    'scatter_color': '#3b82f6',  # blue-500
}


def _setup_dark_theme(ax: plt.Axes, fig: plt.Figure) -> None:
    """Apply dark theme to matplotlib figure and axes."""
    fig.patch.set_facecolor(DARK_THEME['bg_color'])
    ax.set_facecolor(DARK_THEME['plot_bg'])
    ax.tick_params(colors=DARK_THEME['text_color'])
    ax.xaxis.label.set_color(DARK_THEME['text_color'])
    ax.yaxis.label.set_color(DARK_THEME['text_color'])
    ax.title.set_color(DARK_THEME['text_color'])
    for spine in ax.spines.values():
        spine.set_color(DARK_THEME['grid_color'])
    ax.grid(True, color=DARK_THEME['grid_color'], alpha=0.3)


def _fig_to_base64(fig: plt.Figure, dpi: int = 100) -> str:
    """Convert matplotlib figure to base64-encoded PNG."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close(fig)
    return f"data:image/png;base64,{img_base64}"


def render_plot_2d(plot_data: "PlotData2D") -> str:
    """Render a 2D line plot to base64 PNG."""
    fig, ax = plt.subplots(figsize=(8, 5))
    _setup_dark_theme(ax, fig)

    ax.plot(plot_data.x_values, plot_data.y_values,
            color=DARK_THEME['line_color'], linewidth=2)

    if plot_data.title:
        ax.set_title(plot_data.title)
    ax.set_xlabel(plot_data.x_label)
    ax.set_ylabel(plot_data.y_label)

    return _fig_to_base64(fig)


def render_plot_3d(plot_data: "PlotData3D") -> str:
    """Render a 3D surface plot to base64 PNG."""
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Dark theme for 3D
    fig.patch.set_facecolor(DARK_THEME['bg_color'])
    ax.set_facecolor(DARK_THEME['plot_bg'])
    ax.tick_params(colors=DARK_THEME['text_color'])
    ax.xaxis.label.set_color(DARK_THEME['text_color'])
    ax.yaxis.label.set_color(DARK_THEME['text_color'])
    ax.zaxis.label.set_color(DARK_THEME['text_color'])
    ax.title.set_color(DARK_THEME['text_color'])
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    X, Y = np.meshgrid(plot_data.x_values, plot_data.y_values)
    Z = np.array(plot_data.z_values)

    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)

    if plot_data.title:
        ax.set_title(plot_data.title)
    ax.set_xlabel(plot_data.x_label)
    ax.set_ylabel(plot_data.y_label)
    ax.set_zlabel(plot_data.z_label)

    return _fig_to_base64(fig)


def render_histogram(hist_data: "HistogramData") -> str:
    """Render a histogram to base64 PNG."""
    fig, ax = plt.subplots(figsize=(8, 5))
    _setup_dark_theme(ax, fig)

    ax.hist(hist_data.values, bins=hist_data.bins,
            color=DARK_THEME['line_color'], edgecolor=DARK_THEME['bg_color'], alpha=0.8)

    if hist_data.title:
        ax.set_title(hist_data.title)
    ax.set_xlabel(hist_data.x_label)
    ax.set_ylabel(hist_data.y_label)

    return _fig_to_base64(fig)


def render_scatter(scatter_data: "ScatterData") -> str:
    """Render a scatter plot to base64 PNG."""
    fig, ax = plt.subplots(figsize=(8, 5))
    _setup_dark_theme(ax, fig)

    ax.scatter(scatter_data.x_values, scatter_data.y_values,
               color=DARK_THEME['scatter_color'], alpha=0.7, s=50)

    if scatter_data.title:
        ax.set_title(scatter_data.title)
    ax.set_xlabel(scatter_data.x_label)
    ax.set_ylabel(scatter_data.y_label)

    return _fig_to_base64(fig)


def render_plot(value: object) -> str | None:
    """Render any plot data type to base64 PNG. Returns None if not a plot type."""
    from mathlang.types.result import PlotData2D, PlotData3D, HistogramData, ScatterData

    if isinstance(value, PlotData2D):
        return render_plot_2d(value)
    elif isinstance(value, PlotData3D):
        return render_plot_3d(value)
    elif isinstance(value, HistogramData):
        return render_histogram(value)
    elif isinstance(value, ScatterData):
        return render_scatter(value)
    return None
