from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

platform = Entity(model="plane", scale=(100,1,100), texture="picturejosh.jpg", texture_scale=(100,100), collider="box")
player = FirstPersonController(model="cube", y=0, origin_y = -0.5)

ammo = 50

wall1 = Entity(model="cube", scale=(20,12,1), color=color.gray, collider = "box", x=0, z=-10)
wall2 = Entity(model="cube", scale=(20,12,1), color=color.gray, collider = "box", x=0, z=30)
wall3 = Entity(model="cube", scale=(40,12,1), color=color.gray, collider = "box", x=-10, z=10, rotation_y=90)
wall4 = Entity(model="cube", scale=(40,12,1), color=color.gray, collider = "box", x=10, z=10, rotation_y=90)

targets = []
bullets = []
for _ in range(11):
    x = random.randrange(-9, 9, 2)
    y = random.randrange(1, 6, 1)
    z = random.randrange(random.randint(0,20), random.randint(20,30), 2)
    target = Entity(model="cube", color=color.white, texture="target.png", scale=(1,1,0.1), dx=0.02,
    position = (x,y,z), collider="box")
    target.collider = BoxCollider(target, size=(2,2,2))
    targets.append(target)


gun = Entity(parent=camera, model="gun/3D/gun.obj", origin_y=-0.5, scale=(0.1, 0.1, 0.1), position = (2, -1, 2.5), colider="box", rotation=(0,-90,0))
player.gun = gun

def input(key):
    global bullets
    global ammo
    if key == "left mouse down" and player.gun:
        bullet = Entity(parent=gun, model="cube", scale=(1000, 0.5, 0.5), position=(0,0.5,0), speed = 5, color=color.blue, collider="box", rotation=90)
        bullets.append(bullet)
        gun.blink(color.white)
        bullet.world_parent = scene 
        ammo -= 1
    if ammo == 0:
        lose = Text(text="You lose all your bullets", scale = 1.5, origin=(0,0), background=True, color=color.blue)
        application.pause


def update():
    if held_keys["escape"]:
        application.quit()

    for target in targets:
        target.x += target.dx
        if target.x > 9:
            target.x = 9
            target.dx *= -1

        if target.x < -9:
            target.x = -9
            target.dx *= -1

    if held_keys["shift"]:
        player.speed = 10
    else:
        player.speed = 5

    if held_keys["r"]:
        player.jump_height = 10
    else:
        player.jump_height = 2
    
    global bullets
    if len(bullets) > 0:
        for bullet in bullets:
            bullet.position += bullet.left * 0.01

            hit_info = bullet.intersects()
            if hit_info.hit:
                if hit_info.entity in targets:
                    targets.remove(hit_info.entity)
                    destroy(hit_info.entity)
                    destroy(bullet)
                    bullets.remove(bullet)
                    if len(targets) == 0:
                        message = Text(text="You are free like a bird!", scale = 1.5, origin=(0,0), background=True, color=color.blue)
                        application.pause



    

if __name__ == "__main__":
    app.run()
