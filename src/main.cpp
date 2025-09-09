#include "bn_core.h"
#include "bn_keypad.h"
#include "bn_sound_items.h"
#include "bn_sprite_text_generator.h"
#include "bn_sprite_font.h"
#include "bn_sprite_ptr.h"
#include "bn_vector.h"
#include "game/game.h"

int main(){
    bn::core::init();

    // Title
    bn::sprite_text_generator txt(bn::sprite_font::system_font());
    bn::vector<bn::sprite_ptr, 64> t;
    txt.set_center_alignment();
    txt.generate(0, -20, "PUFFQUEST ADVANCE", t);
    txt.generate(0, 0, "Press START", t);

    while(!bn::keypad::start_pressed()){
        bn::core::update();
    }

    // Game loop
    auto game = game::GameState::start();
    while(true){
        if(!game.tick()){
            // Game Over
            t.clear();
            txt.generate(0, -10, "GAME OVER", t);
            txt.generate(0, 10, "Press START", t);
            while(!bn::keypad::start_pressed()) bn::core::update();
            game = game::GameState::start();
        }
        bn::core::update();
    }
}
