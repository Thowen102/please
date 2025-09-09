#pragma once
#include "bn_sprite_text_generator.h"
#include "bn_vector.h"


namespace game {
struct UI {
bn::sprite_text_generator text_gen;
bn::vector<bn::sprite_ptr, 64> sprites;
int score = 0;
int hiscore = 0;
bool show_fps = false;


UI(const bn::sprite_font& font);
void draw();
};
}
