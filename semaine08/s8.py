import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go  # type: ignore


from numpy.typing import NDArray
from sklearn.pipeline import Pipeline


def viz3D(model: Pipeline, *data: pd.DataFrame) -> None:
    """
    3D graph of sound velocity in water.

    Uses Matplotlib's interactive 3D plotting.
    """

    salinity: NDArray[np.float64] = np.linspace(0, 40, 100)
    temperature: NDArray[np.float64] = np.linspace(18, 34, 100)

    depth: float = float(
        np.asarray(pd.concat([df.depth for df in data])).mean()
    )

    # Generate prediction grid
    S, T = np.meshgrid(salinity, temperature)

    surf_X = np.column_stack([
        S.ravel(),
        T.ravel(),
        np.full(S.size, depth),
    ])

    surf_y = np.asarray(model.predict(surf_X))
    Z = surf_y.reshape(S.shape)

    # Create figure
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot observed data (one scatter series per DataFrame)
    for i, df in enumerate(data):
        ax.scatter(
            df.salinity,
            df.temperature,
            df.velocity,
            s=16,
            label=f'Data {i + 1}'
        )

    # Plot prediction surface
    ax.plot_surface(
        S,
        T,
        Z,
        cmap='viridis',
        vmin=1400,
        vmax=1600,
        alpha=0.6,
        edgecolor='none'
    )

    # Labels and title
    ax.set_title("Velocity")
    ax.set_xlabel("x: Salinity")
    ax.set_ylabel("y: Temperature")
    ax.set_zlabel("z: Velocity")

    # Legend
    ax.legend(loc='upper left')

    # Camera position (approximation of Plotly camera)
    ax.view_init(elev=10, azim=-135)

    plt.tight_layout()
    plt.show()

def viz3D_plotly(model: Pipeline, *data: pd.DataFrame, renderer: str = 'browser') -> None:
    """
    3D graph of sound velocity in water.

    * renderer: 'browser', 'notebook', 'vscode'
    """
    salinity: NDArray[np.float64] = np.linspace(0, 40, 100)
    temperature: NDArray[np.float64] = np.linspace(18, 34, 100)
    depth: NDArray[np.float64] = np.asarray(pd.concat([df.depth for df in data])).mean()

    surf_X = np.transpose(
        [
            np.tile(salinity, len(temperature)),
            np.repeat(temperature, len(salinity)),
            np.full(len(temperature) * len(salinity), depth),
        ]
    )

    surf_y = np.asarray(model.predict(surf_X))

    fig = go.Figure(
        data=[
            go.Scatter3d(
                z=df.velocity,
                x=df.salinity.values,
                y=df.temperature.values,
                mode="markers",
                marker_size=4,
            )
            for df in data
        ]
        + [
            go.Surface(
                z=surf_y.reshape(100, 100),
                x=salinity,
                y=temperature,
                cmin=1400,
                cmax=1600,
            )
        ]
    )

    fig.update_layout(
        title="Velocity",
        autosize=False,
        width=800,
        height=800,
        margin=dict(l=50, r=50, b=50, t=50),
        scene=dict(
            xaxis=dict(title="x:Salinity"),
            yaxis=dict(title="y:Temperature"),
            zaxis=dict(title="z:Velocity"),
        ),
        legend=dict(xanchor="left", yanchor="top", x=0.01, y=0.99),
        scene_camera=dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=-1.25, y=-1.25, z=0.25),
        ),
    )

    fig.show(renderer=renderer)
