#pragma once
#include "bn_fixed.h"


namespace cfg {
constexpr int screen_w = 240;
constexpr int screen_h = 160;


// Physics
constexpr bn::fixed gravity = 0.26; // pixels/frame^2
constexpr bn::fixed max_fall = 5.0; // terminal velocity
constexpr bn::fixed run_speed = 1.2; // px/frame
constexpr bn::fixed jump_speed = -4.6; // initial impulse


// Procgen
constexpr int chunk_px = 120; // width of a spawn chunk
constexpr int max_platforms = 12;
constexpr int max_enemies = 16;


// Power-up timings (frames @60fps)
constexpr int powerup_time = 60*12;
}
