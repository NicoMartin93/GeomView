module Geometry

using LinearAlgebra
using Dates
using Statistics
using Printf  # Importar el módulo Printf

export expand_rectangle, points_inside_parallelepiped, line_plane_intersection_vectorized, point_in_rectangle_vectorized

function expand_rectangle(center, vertices, normal_vector, prolongacion, theta)
    """
    Expande los vértices de un rectángulo proporcionalmente a lo largo de un vector normal,
    manteniendo la forma del rectángulo original.
    """
    expanded_vertices = []
    for vertex in vertices
        expanded_vertex = vertex .+ (vertex .- center) .* tan(theta)
        expanded_vertex += prolongacion .* normal_vector
        push!(expanded_vertices, expanded_vertex)
    end
    return hcat(expanded_vertices...)'
end

function points_inside_parallelepiped(points, vertices)
    """
    Determina si una serie de puntos están dentro de un paralelepípedo definido por ocho vértices.

    Args:
        points: Matriz de tamaño (n, 3) - Coordenadas de los puntos a verificar.
        vertices: Matriz de tamaño (8, 3) - Coordenadas de los 8 vértices del paralelepípedo.

    Returns:
        Vector de booleanos de tamaño n - Verdadero si el punto está dentro del paralelepípedo, Falso en caso contrario.
    """
    # Divide los vértices en dos grupos opuestos para definir las seis caras
    faces = [
        (vertices[1, :], vertices[2, :], vertices[3, :], vertices[4, :]),  # Cara 1
        (vertices[1, :], vertices[4, :], vertices[5, :], vertices[8, :]),  # Cara 2
        (vertices[1, :], vertices[2, :], vertices[5, :], vertices[6, :]),  # Cara 3
        (vertices[2, :], vertices[3, :], vertices[6, :], vertices[7, :]),  # Cara 4
        (vertices[5, :], vertices[6, :], vertices[7, :], vertices[8, :]),  # Cara 5
        (vertices[4, :], vertices[3, :], vertices[8, :], vertices[7, :])   # Cara 6
    ]

    # Punto de referencia dentro del paralelepípedo (centroide)
    centroid = mean(vertices, dims=1)[:]

    # Inicializar vector de booleanos
    inside = trues(size(points, 1))

    # Verificar cada cara para todos los puntos
    for (v0, v1, v2, v3) in faces
        # Vector normal de la cara a partir de tres puntos
        normal_vector = cross(v1 - v0, v2 - v0)

        # Productos escalares para el punto de referencia y los puntos a verificar
        reference_sign = dot(normal_vector, centroid - v0)
        v0_broadcast = reshape(v0, 1, :)  # Convertir v0 a (1, 3) para transmisión
        points_sign = sum((points .- v0_broadcast) .* normal_vector', dims=2)[:]

        # points_sign = (points .- v0) * normal_vector

        # Marcar como false los puntos que están fuera de esta cara
        inside .&= sign.(points_sign) .== sign(reference_sign)
    end

    return inside
end

function line_plane_intersection_vectorized(line_points, line_dirs, plane_point, plane_normal)
    """
    Calcula la intersección entre múltiples líneas y un plano definido.

    Args:
        line_points: Matriz de tamaño (n, 3) - Puntos de inicio de las líneas.
        line_dirs: Matriz de tamaño (n, 3) - Direcciones de las líneas.
        plane_point: Vector de tamaño (3,) - Punto en el plano.
        plane_normal: Vector de tamaño (3,) - Vector normal al plano.

    Returns:
        Matriz de tamaño (n, 3) con los puntos de intersección.
    """
    # Vector desde los puntos de las líneas al punto del plano
    diff = line_points .- reshape(plane_point, 1, :)

    # Producto punto entre la dirección de las líneas y la normal del plano
    denom = sum(line_dirs .* reshape(plane_normal, 1, :), dims=2)  # Producto escalar fila por fila

    # Producto punto entre diff y la normal del plano
    numer = sum(diff .* reshape(plane_normal, 1, :), dims=2)  # Producto escalar fila por fila

    # Parámetro t para la intersección
    t = -numer ./ denom

    # Puntos de intersección
    intersections = line_points .+ t .* line_dirs

    return intersections
end

function point_in_rectangle_vectorized(points, rect_vertices)
    """
    Verifica si los puntos están dentro de un rectángulo definido por sus vértices.

    Args:
        points: Matriz de tamaño (n, 3) - Puntos a verificar.
        rect_vertices: Matriz de tamaño (4, 3) - Coordenadas de los vértices del rectángulo.

    Returns:
        Vector booleano de tamaño (n,) indicando si cada punto está dentro del rectángulo.
    """
    # Asegurar que rect_vertices tiene la forma correcta
    if size(rect_vertices, 1) != 4 || size(rect_vertices, 2) != 3
        throw(ArgumentError("rect_vertices debe ser de tamaño (4, 3)."))
    end

    # Vectores del rectángulo
    v1 = rect_vertices[2, :] .- rect_vertices[1, :]
    v2 = rect_vertices[4, :] .- rect_vertices[1, :]

    # Proyectar los puntos en el sistema de coordenadas del rectángulo
    diff = points .- reshape(rect_vertices[1, :], 1, :)
    u = sum(diff .* reshape(v1, 1, :), dims=2) ./ sum(v1 .* v1)
    v = sum(diff .* reshape(v2, 1, :), dims=2) ./ sum(v2 .* v2)

    # Verificar si los puntos están dentro del rango [0, 1] en ambas direcciones
    inside = (u .>= 0) .& (u .<= 1) .& (v .>= 0) .& (v .<= 1)

    return inside
end

end
