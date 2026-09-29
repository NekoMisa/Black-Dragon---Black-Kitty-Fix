/**
 * @file velocityAlphaV.glsl
 *
 * $LicenseInfo:firstyear=2007&license=viewerlgpl$
 * Second Life Viewer Source Code
 * Copyright (C) 2007, Linden Research, Inc.
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation;
 * version 2.1 of the License only.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 *
 * Linden Research, Inc., 945 Battery Street, San Francisco, CA  94111  USA
 * $/LicenseInfo$
 */

#ifdef RIGGED_PRECISE_MATH
invariant gl_Position;
precise gl_Position;
#endif

uniform mat4 modelview_projection_matrix;
uniform mat4 modelview_matrix;
uniform mat4 projection_matrix;
uniform mat4 last_modelview_matrix;
uniform mat4 last_object_matrix;
uniform mat4 texture_matrix0;

in vec3 position;
in vec4 diffuse_color;
in vec2 texcoord0;

out vec2 vary_texcoord0;
out vec4 vertex_color;

void passTextureIndex();
void writeVaryVelocity(vec4 pos, vec4 last_pos);

#ifdef HAS_SKIN
mat3x4 getSkinBlend();
mat3x4 getLastSkinBlend();
vec4 skinTransformH(mat3x4 skin, vec3 position, mat4 transform);
vec4 lastSkinTransformH(mat3x4 skin, vec3 position, mat4 transform);
#endif

void main()
{
    vary_texcoord0 = (texture_matrix0 * vec4(texcoord0, 0, 1)).xy;
    vertex_color = diffuse_color;

    passTextureIndex();

#ifdef HAS_SKIN
    vec4 pos = projection_matrix * skinTransformH(getSkinBlend(), position, modelview_matrix);
    gl_Position = pos;

    vec4 last_pos = projection_matrix * lastSkinTransformH(getLastSkinBlend(), position, last_modelview_matrix);
#else
    vec4 pos = modelview_projection_matrix * vec4(position.xyz, 1.0);
    gl_Position = pos;

    vec4 last_pos = projection_matrix * last_modelview_matrix * last_object_matrix * vec4(position.xyz, 1.0);
#endif

    writeVaryVelocity(pos, last_pos);
}
