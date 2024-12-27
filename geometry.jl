
module Geometry

export expand_rectangle, points_inside_parallelepiped, line_plane_intersection_vectorized, point_in_rectangle_vectorized

function expand_rectangle(center, vertices, normal_vector, prolongacion, theta)
    expanded_vertices = [vertex + (vertex - center) * tan(theta) + prolongacion * normal_vector for vertex in vertices]
    return hcat(expanded_vertices...)
end

function points_inside_parallelepiped(points, vertices)
    faces = [
        (vertices[:, 1], vertices[:, 2], vertices[:, 3], vertices[:, 4]),
        (vertices[:, 1], vertices[:, 4], vertices[:, 5], vertices[:, 8]),
        (vertices[:, 1], vertices[:, 2], vertices[:, 5], vertices[:, 6]),
        (vertices[:, 2], vertices[:, 3], vertices[:, 6], vertices[:, 7]),
        (vertices[:, 5], vertices[:, 6], vertices[:, 7], vertices[:, 8]),
        (vertices[:, 4], vertices[:, 3], vertices[:, 8], vertices[:, 7])
    ]
    centroid = mean(vertices, dims=2)
    inside = trues(size(points, 2))
    for (v0, v1, v2, v3) in faces
        normal_vector = cross(v1 - v0, v2 - v0)
        reference_sign = dot(normal_vector, centroid - v0)
        points_sign = dot.(eachcol(points .- v0), Ref(normal_vector))
        inside .&= sign.(points_sign) .== sign(reference_sign)
    end
    return inside
end

function line_plane_intersection_vectorized(line_points, line_dirs, plane_point, plane_normal)
    denom = dot.(eachcol(line_dirs), Ref(plane_normal))
    parallel_mask = isapprox.(denom, 0.0)
    t = dot(plane_normal, plane_point) .- dot.(plane_normal, eachcol(line_points)) ./ denom
    t[parallel_mask] .= NaN
    intersection_points = line_points .+ t .* line_dirs
    intersection_points[t .< 0, :] .= NaN
    return intersection_points
end

function point_in_rectangle_vectorized(points, rect_vertices)
    v0, v1, v3 = rect_vertices[:, 1], rect_vertices[:, 2], rect_vertices[:, 4]
    edge1 = v1 - v0
    edge2 = v3 - v0
    vp = points .- v0
    dot11 = dot(edge1, edge1)
    dot12 = dot(edge1, edge2)
    dot22 = dot(edge2, edge2)
    dot1p = dot.(eachcol(edge1), eachcol(vp))
    dot2p = dot.(eachcol(edge2), eachcol(vp))
    inv_denom = 1 / (dot11 * dot22 - dot12^2)
    u = (dot22 * dot1p .- dot12 * dot2p) .* inv_denom
    v = (dot11 * dot2p .- dot12 * dot1p) .* inv_denom
    inside_rectangle = (0 .<= u) .& (u .<= 1) .& (0 .<= v) .& (v .<= 1)
    return inside_rectangle
end

end
