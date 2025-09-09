#include "game/ui.h"
#include "bn_core.h"
#include "bn_sprite_text_generator.h"
#include "bn_sprite_items_enemies.h"


using namespace bn; using namespace game;


UI::UI(const sprite_font& font): text_gen(font){ text_gen.set_center_alignment(); }


void UI::draw(){
sprites.clear();
text_gen.generate(0, -70, "SCORE " + bn::to_string<16>(score), sprites);
}
