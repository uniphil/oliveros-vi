#ifdef GL_ES
precision mediump float;
#endif

/*
HUSL-GLSL v3.2
HUSL is a human-friendly alternative to HSL. ( http://www.husl-colors.org )
GLSL port by William Malo ( https://github.com/williammalo )
Put this code in your fragment shader.
*/
vec3 husl_intersectLineLine(vec3 line1x, vec3 line1y, vec3 line2x, vec3 line2y) {
    return (line1y - line2y) / (line2x - line1x);
}
vec3 husl_distanceFromPole(vec3 pointx,vec3 pointy) {
    return sqrt(pointx*pointx + pointy*pointy);
}
vec3 husl_lengthOfRayUntilIntersect(float theta, vec3 x, vec3 y) {
    vec3 len = y / (sin(theta) - x * cos(theta));
    if (len.r < 0.0) {len.r=1000.0;}
    if (len.g < 0.0) {len.g=1000.0;}
    if (len.b < 0.0) {len.b=1000.0;}
    return len;
}
float husl_maxSafeChromaForL(float L){
    mat3 m2 = mat3(
        vec3( 3.2409699419045214  ,-0.96924363628087983 , 0.055630079696993609),
        vec3(-1.5373831775700935  , 1.8759675015077207  ,-0.20397695888897657 ),
        vec3(-0.49861076029300328 , 0.041555057407175613, 1.0569715142428786  )
    );
    float sub1 = pow(L + 16.0, 3.0) / 1560896.0;
    float sub2 = sub1 > 0.0088564516790356308 ? sub1 : L / 903.2962962962963;
    vec3 top1   = (284517.0 * m2[0] - 94839.0  * m2[2]) * sub2;
    vec3 bottom = (632260.0 * m2[2] - 126452.0 * m2[1]) * sub2;
    vec3 top2   = (838422.0 * m2[2] + 769860.0 * m2[1] + 731718.0 * m2[0]) * L * sub2;
    vec3 bounds0x = top1 / bottom;
    vec3 bounds0y = top2 / bottom;
    vec3 bounds1x =              top1 / (bottom+126452.0);
    vec3 bounds1y = (top2-769860.0*L) / (bottom+126452.0);
    vec3 xs0 = husl_intersectLineLine(bounds0x, bounds0y, -1.0/bounds0x, vec3(0.0) );
    vec3 xs1 = husl_intersectLineLine(bounds1x, bounds1y, -1.0/bounds1x, vec3(0.0) );
    vec3 lengths0 = husl_distanceFromPole( xs0, bounds0y + xs0 * bounds0x );
    vec3 lengths1 = husl_distanceFromPole( xs1, bounds1y + xs1 * bounds1x );
    return  min(lengths0.r,
            min(lengths1.r,
            min(lengths0.g,
            min(lengths1.g,
            min(lengths0.b,
                lengths1.b)))));
}
float husl_maxChromaForLH(float L, float H) {
    float hrad = radians(H);
    mat3 m2 = mat3(
        vec3( 3.2409699419045214  ,-0.96924363628087983 , 0.055630079696993609),
        vec3(-1.5373831775700935  , 1.8759675015077207  ,-0.20397695888897657 ),
        vec3(-0.49861076029300328 , 0.041555057407175613, 1.0569715142428786  )
    );
    float sub1 = pow(L + 16.0, 3.0) / 1560896.0;
    float sub2 = sub1 > 0.0088564516790356308 ? sub1 : L / 903.2962962962963;
    vec3 top1   = (284517.0 * m2[0] - 94839.0  * m2[2]) * sub2;
    vec3 bottom = (632260.0 * m2[2] - 126452.0 * m2[1]) * sub2;
    vec3 top2   = (838422.0 * m2[2] + 769860.0 * m2[1] + 731718.0 * m2[0]) * L * sub2;
    vec3 bound0x = top1 / bottom;
    vec3 bound0y = top2 / bottom;
    vec3 bound1x =              top1 / (bottom+126452.0);
    vec3 bound1y = (top2-769860.0*L) / (bottom+126452.0);
    vec3 lengths0 = husl_lengthOfRayUntilIntersect(hrad, bound0x, bound0y );
    vec3 lengths1 = husl_lengthOfRayUntilIntersect(hrad, bound1x, bound1y );
    return  min(lengths0.r,
            min(lengths1.r,
            min(lengths0.g,
            min(lengths1.g,
            min(lengths0.b,
                lengths1.b)))));
}
float husl_fromLinear(float c) {
    return c <= 0.0031308 ? 12.92 * c : 1.055 * pow(c, 1.0 / 2.4) - 0.055;
}
float husl_toLinear(float c) {
    return c > 0.04045 ? pow((c + 0.055) / (1.0 + 0.055), 2.4) : c / 12.92;
}
vec3 husl_toLinear(vec3 c) {
    return vec3( husl_toLinear(c.r), husl_toLinear(c.g), husl_toLinear(c.b) );
}
float husl_yToL(float Y){
    return Y <= 0.0088564516790356308 ? Y * 903.2962962962963 : 116.0 * pow(Y, 1.0 / 3.0) - 16.0;
}
float husl_lToY(float L) {
    return L <= 8.0 ? L / 903.2962962962963 : pow((L + 16.0) / 116.0, 3.0);
}
vec3 xyzToRgb(vec3 tuple) {
    return vec3(
        husl_fromLinear(dot(vec3( 3.2409699419045214  ,-1.5373831775700935 ,-0.49861076029300328 ), tuple.rgb )),//r
        husl_fromLinear(dot(vec3(-0.96924363628087983 , 1.8759675015077207 , 0.041555057407175613), tuple.rgb )),//g
        husl_fromLinear(dot(vec3( 0.055630079696993609,-0.20397695888897657, 1.0569715142428786  ), tuple.rgb )) //b
    );
}
vec3 luvToXyz(vec3 tuple) {
    float L = tuple.x;
    float varU = tuple.y / (13.0 * L) + 0.19783000664283681;
    float varV = tuple.z / (13.0 * L) + 0.468319994938791;
    float Y = husl_lToY(L);
    float X = 0.0 - (9.0 * Y * varU) / ((varU - 4.0) * varV - varU * varV);
    float Z = (9.0 * Y - (15.0 * varV * Y) - (varV * X)) / (3.0 * varV);
    return vec3(X, Y, Z);
}
vec3 lchToLuv(vec3 tuple) {
    float hrad = radians(tuple.b);
    return vec3(
        tuple.r,
        cos(hrad) * tuple.g,
        sin(hrad) * tuple.g
    );
}
vec3 huslToLch(vec3 tuple) {
    tuple.g *= husl_maxChromaForLH(tuple.b, tuple.r) / 100.0;
    return tuple.bgr;
}
vec3 huslpToLch(vec3 tuple) {
    tuple.g *= husl_maxSafeChromaForL(tuple.b) / 100.0;
    return tuple.bgr;
}
vec3 lchToRgb(vec3 tuple) {
    return xyzToRgb(luvToXyz(lchToLuv(tuple)));
}
vec3 huslToRgb(vec3 tuple) {
    return lchToRgb(huslToLch(tuple));
}
vec3 huslpToRgb(vec3 tuple) {
    return lchToRgb(huslpToLch(tuple));
}
// allow vec4's
vec4  huslToRgb(vec4 c) {return vec4(  huslToRgb( vec3(c.x,c.y,c.z) ), c.a);}
vec4 huslpToRgb(vec4 c) {return vec4( huslpToRgb( vec3(c.x,c.y,c.z) ), c.a);}
// allow 3 floats
vec3  huslToRgb(float x, float y, float z) {return  huslToRgb( vec3(x,y,z) );}
vec3 huslpToRgb(float x, float y, float z) {return huslpToRgb( vec3(x,y,z) );}
// allow vec2
vec4  hvToRgb(vec2 hv) {return  huslToRgb( vec4(hv.x*360.,100.,hv.y*100.,1.) );}
/*
END HUSL-GLSL
*/

#define H 720
#define W 1280
#define START 1.
#define END 10.
#define OFFSET 0.

uniform vec2 u_resolution;
uniform float u_time;
float t;

float rand(vec2 co) {
    return fract(sin(dot(co.xy, vec2(12.9898, 78.233))) * 43758.5453);
}

vec2 colourize(float v, float p1, float p2) {
  float h, o;
  if (v < 0.5) {
    h = t / p1 / 10.;
    o = 1. - (v * 2.);
  } else {
    h = -t / p2 / 10.;
    o =(v - 0.5) * 2.;
  }
  return vec2(mod(h, 1.), pow(o, 2.) * .4);
}

vec2 rotate(vec2 p, float theta) {
  return vec2(
    p.x * cos(theta) - p.y * sin(theta),
    p.x * sin(theta) + p.y * cos(theta)
  );
}

float grid(vec2 p) {
  return sin(
    (
      (
        sin(p.x / 100.)  // macro pattern x frequency
        + sin(p.y / 100.)  // macro pattern y frequency
      ) / 4. + 0.5  // shift -2..2 to 0..1
    ) * 24.  // get multiple cycles from valley to peak
    + sin(t / 11.)  // animate!
      * 11.  // animation range
  ) / 2. + 0.5;  // shift -1..1 to 0..1
}

float pipes(vec2 p) {
  return sin(
    p.x / 23.  // basic pipe
    + t / 5.  // animate globally
    + sin(
      p.x / 31.  // interference waves
      + t / 2.  // animate the interference
    )
  ) / 2. + 0.5;  // shift range
}

float waves(vec2 p) {
  return (
    sin(
      p.x / 41.
      + sin(p.y * sin(t / 20.) / 50.)
    )
    + sin(
      p.x / 33.
      + sin(t / 10.) * 5.
    )
  ) / 4. + 0.5;
}

float circle(vec2 p) {
  float r = sqrt(
    pow(p.x + sin(t / 17.) * float(W / 4), 2.)
    + pow(p.y + sin(t / 79.) * float(H / 4), 2.)
    + 10000.  // centre point avoidance
  );
  return sin(
    r / 42.  // feature size
    + sin(t / 30.) * 20.  // animate!
  ) / 2. + 0.5;
}

float radgrad(vec2 p) {
  float r = sqrt(
    pow(p.x + sin(t / 17.) * float(W / 4), 2.)
    + pow(p.y + sin(t / 79.) * float(H / 4), 2.)
    + 100000.
  );
  return (1. - r / float(H));
}

#define FADE 100.

float mask() {
  vec2 p = gl_FragCoord.xy;
  float xfade = 1.;
  float yfade = 1.;
  if (p.x < FADE) {
    xfade = p.x / FADE;
  } else if (float(W) - p.x < FADE) {
    xfade = (float(W) - p.x) / FADE;
  }
  if (p.y < FADE) {
    yfade = p.y / FADE;
  } else if (float(H) - p.y < FADE) {
    yfade = (float(H) - p.y) / FADE;
  }
  return 1. * xfade * yfade;
}

float show_window() {
  if (u_time < START - 0.5) {
    return 0.;
  } else if (u_time < START + 0.5) {
    return u_time - (START - 0.5);
  } else if (u_time < END - 0.5) {
    return 1.;
  } else if (u_time < END + 0.5) {
    return (END + 0.5) - u_time;
  } else {
    return 0.;
  }
}

void main() {
  t = u_time + OFFSET;
  vec2 p = (gl_FragCoord.xy - vec2(W / 2, H / 2)) * (sin(t / 80.) + 6.) / 3.;  // / 4.

  float g = grid(rotate(p, sin(t / 27.) / 3.) / 7.);
  float pip = pipes(rotate(p, sin(-t / 38.) / 5.) / 7.);
  float w = waves(p / 3.);
  float c = circle(p / 4.);
  float l1v = (g + pip) / 2.;
  float l2v = (w + c) / 2.;

  gl_FragColor = (
    hvToRgb(colourize(l1v, 7., 13.)) +
    hvToRgb(colourize(l2v, 11., 17.))
    + hvToRgb(vec2(sin(.4 + t / 20.) / 2. + .5, radgrad(p) / 3.))
  ) / 1. * (.5 * rand(p) + .5) * mask() * show_window();
}
