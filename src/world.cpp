#include "game/world.h"
#include "bn_random.h"
#include "bn_sprite_items_tiles.h"
#include "bn_sprite_items_enemies.h"
#include "bn_keypad.h"


using namespace bn; using namespace game;


static random g_rng;


static sprite_ptr make_tile(int x, int y, int tile_index){
// tiles.bmp arranged 32x32; frame index selects tile
auto s = sprite_items::tiles.create_sprite(x,y);
s.set_tiles(sprite_items::tiles.tiles_item().create_tiles(tile_index));
s.set_bg_priority(2);
return s;
}


void World::spawn_chunk(int start_x){
// Ground platform
int ground_y = 72; // y coord
for(int i=0;i<cfg::chunk_px;i+=32){
platforms.push_back(Platform{ make_tile(start_x + i, ground_y, 0) });
}
// Random floating platforms, enemies, pickups
int n = 1 + g_rng.get_int(0, 2);
for(int i=0;i<n;i++){
int px = start_x + 40 + g_rng.get_int(0, cfg::chunk_px-80);
int py = 20 + g_rng.get_int(0, 60);
platforms.push_back(Platform{ make_tile(px, py, 1) });
// enemies
if(g_rng.get_int(0,1)){
auto e = sprite_items::enemies.create_sprite(px, py-16);
e.set_bg_priority(1);
enemies.push_back( Enemy{ bn::move(e), EnemyKind::Walker, { g_rng.get_bool()? fixed(0.4f): fixed(-0.4f), 0 } } );
}
// pickup
if(g_rng.get_int(0,2)==0){
auto p = sprite_items::tiles.create_sprite(px+12, py-20);
pickups.push_back( Pickup{ bn::move(p), Ability::Dash } );
}
}
}


void World::update(){
// Auto scroll
scroll_x += 1;
for(auto& pl : platforms){ pl.spr.set_x(pl.spr.x() - 1); }
for(auto& en : enemies){ en.spr.set_x(en.spr.x() - 1 + en.vel.x()); }
for(auto& pk : pickups){ pk.spr.set_x(pk.spr.x() - 1); }


// Cull off‑screen
auto off = [](const sprite_ptr& s){ return s.x() < -140; };
platforms.erase( remove_if(platforms.begin(), platforms.end(), [&](auto& p){ return off(p.spr); }), platforms.end());
enemies.erase( remove_if(enemies.begin(), enemies.end(), [&](auto& e){ return off(e.spr); }), enemies.end());
pickups.erase( remove_if(pickups.begin(), pickups.end(), [&](auto& p){ return off(p.spr); }), pickups.end());


// Spawn new chunk when needed
if(platforms.empty() || platforms.back().spr.x() < 140){
spawn_chunk(scroll_x + 240);
}
}
