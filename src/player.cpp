#include "game/player.h"
#include "bn_keypad.h"
#include "bn_sound_items.h"
#include "bn_sprite_items_player.h"
#include "game/config.h"


using namespace bn;
using namespace game;


Player Player::create(int x, int y){
auto spr = sprite_items::player.create_sprite(x,y);
spr.set_bg_priority(1);
Player p{ bn::move(spr) };
return p;
}


void Player::hit(){
if(hp>0){ --hp; }
sound_items::hit.play();
}


void Player::update(){
// Input → horizontal
fixed ax = 0;
if(keypad::left_held()) ax -= cfg::run_speed;
if(keypad::right_held()) ax += cfg::run_speed;
vel.set_x(ax);


// Jump
if(on_ground && keypad::a_pressed()){
vel.set_y(cfg::jump_speed);
sound_items::jump.play();
on_ground = false;
}


// Gravity
vel.set_y(bn::min(vel.y() + cfg::gravity, cfg::max_fall));


// Apply
auto pos = spr.position();
pos.set_x(pos.x() + vel.x());
pos.set_y(pos.y() + vel.y());


// Floor
if(pos.y() > 56){ pos.set_y(56); vel.set_y(0); on_ground = true; }


spr.set_position(pos);


// Ability timer
if(ability != Ability::None && ability_timer>0){
--ability_timer;
if(ability_timer==0) ability = Ability::None;
}
}
