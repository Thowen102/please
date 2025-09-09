#include "game/game.h"
#include "bn_core.h"
#include "bn_keypad.h"
#include "bn_sound_items.h"
#include "bn_regular_bg_map_cell_info.h"
#include "bn_sprite_text_generator.h"
#include "bn_sprite_font.h"


using namespace bn; using namespace game;


GameState GameState::start(){
GameState g{ Player::create(-60, 56), World{}, UI(bn::sprite_font::system_font()) };
g.world.spawn_chunk(0);
return g;
}


bool GameState::tick(){
if(keypad::start_pressed()){ paused = !paused; if(paused) sound_items::pause.play(); }
if(paused){ return true; }


player.update();
world.update();


// Simple collision checks with enemies (AABB)
for(auto it = world.enemies.begin(); it != world.enemies.end(); ){
auto& e = *it;
if(e.spr.bounding_box().intersects(player.spr.bounding_box())){
player.hit();
it = world.enemies.erase(it);
} else {
++it;
}
}


// Pickups → grant Dash for MVP
for(auto it = world.pickups.begin(); it != world.pickups.end(); ){
auto& p = *it;
if(p.spr.bounding_box().intersects(player.spr.bounding_box())){
player.ability = p.ability; player.ability_timer = cfg::powerup_time;
sound_items::collect.play();
it = world.pickups.erase(it);
} else { ++it; }
}


// Score: distance + leftovers
distance += 1; ui.score = distance;
ui.draw();


return player.hp > 0;
}
