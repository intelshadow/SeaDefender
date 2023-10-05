import math
import random
import arcade
import arcade.gui
import os

SPRITE_SCALING_PLAYER = 0.3
SPRITE_BARCO_PESQUERO = 0.6
SPRITE_TIBURON = 0.7
SPRITE_SCALING_BULLET = 1
SPRITE_SCALING_COIN = 0.4
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BULLET_SPEED = 8
VEL_ARPON = 3
MOVEMENT_SPEED = 3
an_vel = 10
ENEMY_MOVEMENT = 4
Volumen_sonido=0.1
nivel_superado=1
MUSIC = [".."+os.path.sep+"assets"+os.path.sep+"music"+os.path.sep+"Musica Sea_Defender.mp3"]
lista_musica = arcade.load_sound(MUSIC[0])
media_player = lista_musica.play()
media_player.volume -= 0.8
Background_layer = "Fondo"
Obtaculos_layer = "Puntuacion"
Piedras_layer = "Colisiones"

seconds = 0


class SonidoView(arcade.View):
    def __init__(self, PauseView, screen_center_y):
        super().__init__()
        self.PauseView = PauseView
        self.media_player = None
        self.paused = False
        self.songs = [":resources:music"+os.path.sep+"funkyrobot.mp3",
                      ":resources:music"+os.path.sep+"1918.mp3"]
        self.cur_song_index = 0

        self.my_music = arcade.load_sound(self.songs[self.cur_song_index])

        self.ui_manager = arcade.gui.UIManager(self.window)

        box = arcade.gui.UIBoxLayout(vertical=False)
        box1 = arcade.gui.UIBoxLayout(vertical=False)

        normal_texture = arcade.load_texture(":resources:onscreen_controls"+os.path.sep+"flat_dark"+os.path.sep+""
                                             "sound_off.png")
        hover_texture = arcade.load_texture(":resources:onscreen_controls"+os.path.sep+"shaded_dark"+os.path.sep+""
                                            "sound_off.png")
        press_texture = arcade.load_texture(":resources:onscreen_controls"+os.path.sep+"shaded_dark"+os.path.sep+""
                                            "sound_off.png")

        self.start_button = arcade.gui.UITextureButton(
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
        )

        self.start_button.on_click = self.start_button_clicked

        box.add(self.start_button)

        press_texture = arcade.load_texture(":resources:onscreen_controls"+os.path.sep+"shaded_dark"+os.path.sep+"down.png")
        normal_texture = arcade.load_texture(":resources:onscreen_controls"+os.path.sep+"flat_dark"+os.path.sep+"down.png")
        hover_texture = arcade.load_texture(":resources:onscreen_controls"+os.path.sep+"shaded_dark"+os.path.sep+"down.png")

        self.down_button = arcade.gui.UITextureButton(
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
        )

        self.down_button.on_click = self.volume_down  # type: ignore
        self.down_button.scale(0.5)

        box.add(self.down_button)

        press_texture = arcade.load_texture(":resources:onscreen_controls"+os.path.sep+"shaded_dark"+os.path.sep+"up.png")
        normal_texture = arcade.load_texture(":resources:onscreen_controls"+os.path.sep+"flat_dark"+os.path.sep+"up.png")
        hover_texture = arcade.load_texture(":resources:onscreen_controls"+os.path.sep+"shaded_dark"+os.path.sep+"up.png")

        self.up_button = arcade.gui.UITextureButton(
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
        )
        self.up_button.on_click = self.volume_up
        self.up_button.scale(0.5)

        box.add(self.up_button)
        press_texture = arcade.load_texture(":resources:onscreen_controls"+os.path.sep+"shaded_dark"+os.path.sep+"right.png")
        normal_texture = arcade.load_texture(":resources:onscreen_controls"+os.path.sep+"flat_dark"+os.path.sep+"right.png")
        hover_texture = arcade.load_texture(":resources:onscreen_controls"+os.path.sep+"shaded_dark"+os.path.sep+"right.png")
        self.right_button = arcade.gui.UITextureButton(
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
        )
        self.right_button.on_click = self.forward
        self.right_button.scale(0.5)
        box.add(self.right_button)
        self.ui_manager.add(arcade.gui.UIAnchorWidget(child=box1))
        self.ui_manager.add(arcade.gui.UIAnchorWidget(child=box))

        press_texture = arcade.load_texture(".."+os.path.sep+"assets"+os.path.sep+"images"+os.path.sep+"Menu_Sonido.png ")
        normal_texture = arcade.load_texture(".."+os.path.sep+"assets"+os.path.sep+"images"+os.path.sep+"Menu_Sonido.png ")
        hover_texture = arcade.load_texture(".."+os.path.sep+"assets"+os.path.sep+"images"+os.path.sep+"Menu_Sonido.png ")
        self.texture = arcade.gui.UITextureButton(
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
        )
        self.texture.scale(1)
        box1.add(self.texture)

        self.screen_center_y = screen_center_y

    def music_over(self):
        self.media_player.pop_handlers()
        self.media_player = None
        self.sound_button_off()
        self.cur_song_index += 1
        if self.cur_song_index >= len(self.songs):
            self.cur_song_index = 0
        self.my_music = arcade.load_sound(self.songs[self.cur_song_index])
        self.media_player = self.my_music.play()
        self.media_player.push_handlers(on_eos=self.music_over)

    def volume_down(self, *_):
        if media_player and media_player.volume > 0.2:
            media_player.volume -= 0.2

    def volume_up(self, *_):
        if media_player and media_player.volume < 1.0:
            media_player.volume += 0.2

    def forward(self, *_):
        skip_time = 10

        if media_player and media_player.time < lista_musica.get_length() - skip_time:
            media_player.seek(media_player.time + 10)

    def sound_button_on(self):
        self.start_button.texture_pressed = \
            arcade.load_texture(":resources:onscreen_controls"+os.path.sep+"shaded_dark"+os.path.sep+"sound_on.png")
        self.start_button.texture = \
            arcade.load_texture(":resources:onscreen_controls"+os.path.sep+"flat_dark"+os.path.sep+"sound_on.png")
        self.start_button.texture_hovered = \
            arcade.load_texture(":resources:onscreen_controls"+os.path.sep+"shaded_dark"+os.path.sep+"sound_on.png")

    def sound_button_off(self):
        self.start_button.texture_pressed = \
            arcade.load_texture(":resources:onscreen_controls"+os.path.sep+"shaded_dark"+os.path.sep+"sound_off.png")
        self.start_button.texture = \
            arcade.load_texture(":resources:onscreen_controls"+os.path.sep+"flat_dark"+os.path.sep+"sound_off.png")
        self.start_button.texture_hovered = \
            arcade.load_texture(":resources:onscreen_controls"+os.path.sep+"shaded_dark"+os.path.sep+"sound_off.png")

    def start_button_clicked(self, *_):
        self.paused = False
        if not media_player:
            # Play button has been hit, and we need to start playing from the beginning.

            media_player.push_handlers(on_eos=self.music_over)
            self.sound_button_on()
        elif not media_player.playing:
            # Play button hit, and we need to un-pause our playing.
            media_player.play()
            self.sound_button_on()
        elif media_player.playing:
            # We are playing music, so pause.
            media_player.pause()
            self.sound_button_off()

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()

        if media_player:
            seconds = media_player.time
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)
            arcade.draw_text(f"Time: {minutes}:{seconds:02}",
                             start_x=10, start_y=10, color=arcade.color.BLACK, font_size=24)
            volume = media_player.volume
            arcade.draw_text(f"Volume: {volume:3.1f}",
                             start_x=10, start_y=50, color=arcade.color.BLACK, font_size=24)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.ALMOND)


        self.ui_manager.enable()

    def on_hide_view(self):

        self.ui_manager.disable()

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.PauseView)


class player(arcade.Sprite):
    def __init__(self, filename, SPRITE_SCALING_PLAYER):
        super().__init__(filename, SPRITE_SCALING_PLAYER)
        self.speed = 0
        self.respawning = 0
        self.vida = 4
        self.respawn()
        self.limite = False
        self.largo = SCREEN_WIDTH
        self.largo_minimo = 20
        self.up = False
        self.animacion = 0
        self.texture = arcade.load_texture(".."+os.path.sep+"assets"+os.path.sep+"sprites"+os.path.sep+"Barco - forma 1_3.png")
        self.aux_segundos = 0
        self.nivel=1
        self.escudo = False

    def respawn(self):
        self.respawning = 0
        self.change_x = 0
        self.change_y = 0
        self.center_x = 70
        self.center_y = 100

    def update(self):
        self.largo += 2
        self.largo_minimo += 2

        if self.respawning:
            self.respawning += 1
            self.alpha = self.respawning
            if self.respawning > 250:
                self.respawning = 0
                self.alpha = 255
        if self.center_x == 0:
            self.center_x -= self.angle
        elif self.center_x == SCREEN_HEIGHT:
            self.center_x -= self.angle
        if self.center_y >= self.largo:
            self.center_y -= MOVEMENT_SPEED+2
        if self.center_y <= self.largo_minimo-1:

            self.speed = 2
            self.center_y += 2.5

        self.angle = self.change_angle
        self.center_x += self.angle
        self.center_y += self.speed

    def update_animation(self, seconds):
        if self.nivel==1:
            if self.escudo == True:
                self.texture = arcade.load_texture(".."+os.path.sep+"assets"+os.path.sep+"sprites"+os.path.sep+"Escudo - forma 1.png")


            else:
                if seconds - self.aux_segundos > 0.1:
                    if (self.animacion == 3):
                        self.animacion = 0
                    if (self.animacion == 0):
                        self.texture = arcade.load_texture(".."+os.path.sep+"assets"+os.path.sep+"sprites"+os.path.sep+"Barco - forma 1_1.png")
                    elif (self.animacion == 1):
                        self.texture = arcade.load_texture(".."+os.path.sep+"assets"+os.path.sep+"sprites"+os.path.sep+"Barco - forma 1_3.png")
                    elif (self.animacion == 2):
                        self.texture = arcade.load_texture(".."+os.path.sep+"assets"+os.path.sep+"sprites"+os.path.sep+"Barco - forma 1_5.png")
                    self.animacion += 1
                    self.aux_segundos = seconds
        else:
            if self.escudo == True:
                self.texture = arcade.load_texture(
                    ".." + os.path.sep + "assets" + os.path.sep + "sprites" + os.path.sep + "Escudo - forma 2.png")


            else:
                if seconds - self.aux_segundos > 0.1:
                    if (self.animacion == 3):
                        self.animacion = 0
                    if (self.animacion == 0):
                        self.texture = arcade.load_texture(
                            ".." + os.path.sep + "assets" + os.path.sep + "sprites" + os.path.sep + "Barco - forma 2_1.png")
                    elif (self.animacion == 1):
                        self.texture = arcade.load_texture(
                            ".." + os.path.sep + "assets" + os.path.sep + "sprites" + os.path.sep + "Barco - forma 2_3.png")
                    elif (self.animacion == 2):
                        self.texture = arcade.load_texture(
                            ".." + os.path.sep + "assets" + os.path.sep + "sprites" + os.path.sep + "Barco - forma 2_5.png")
                    self.animacion += 1
                    self.aux_segundos = seconds


class pez(arcade.Sprite):
    def __init__(self, filename, sprite_scaling, ):
        super().__init__(filename, sprite_scaling)
        self.vida = 2
        self.speed = 0
        self.numero = 0
        self.control = 0
        self.start_x = 0
        self.start_y = 0
        self.center_x = 0
        self.center_y = 0
        self.action = 60
        self.act0 = 60
        self.limite_abajo = 50
        self.x = 20
        self.y = 20
        self.largo_minimo = 0
        self.largo = SCREEN_WIDTH
        self.s = 60
        self.aux_segundos = 0
        self.animacion = 0
    def update(self):
        self.largo_minimo+=2
        if self.center_y<=self.largo_minimo:
            self.center_y+=700
        if self.s<=60 and self.s>0:
            self.center_y-=3
            self.center_x-=5
            self.control+=2
            self.s-=1
        elif self.act0<=60 and self.act0>0:
            self.center_x+=5
            self.center_y+=2
            self.control+=2
            self.act0-=1
        elif self.action<=60 and self.action>0:
            self.center_y+=6
            self.control+=3
            self.action-=1
        if self.s==0 and self.action==0 and self.act0==0:
            self.s=60
            self.act0=60
            self.action=60

    def update_animation(self, seconds):
        if seconds - self.aux_segundos > 0.1:
            if (self.animacion == 4):
                self.animacion = 0
            if (self.animacion == 0):
                self.texture = arcade.load_texture(
                    ".." + os.path.sep + "assets" + os.path.sep + "sprites" + os.path.sep + "Pez_contaminado_1.png")
            elif (self.animacion == 1):
                self.texture = arcade.load_texture(
                    ".." + os.path.sep + "assets" + os.path.sep + "sprites" + os.path.sep + "Pez_contaminado_2.png")
            elif (self.animacion == 2):
                self.texture = arcade.load_texture(
                    ".." + os.path.sep + "assets" + os.path.sep + "sprites" + os.path.sep + "Pez_contaminado_3.png")
            elif (self.animacion == 3):
                self.texture = arcade.load_texture(
                    ".." + os.path.sep + "assets" + os.path.sep + "sprites" + os.path.sep + "Pez_contaminado_4.png")
            self.animacion += 1
            self.aux_segundos = seconds
class ataque_pez(arcade.Sprite):
    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)
        self.speed = 0
        self.center_x = 0
        self.center_y = 10

    def update(self):
        self.center_y += -BULLET_SPEED+6


class tiburon(arcade.Sprite):
    def __init__(self, filename, sprite_scaling, ):
        super().__init__(filename, sprite_scaling)
        self.vida = 2
        self.aux_segundos = 0
        self.animacion = 0
        self.screen_center_y=0
    def reset_pos(self):


        self.center_y = self.screen_center_y + 900
        self.center_x = random.randrange(70, 530)

    def update(self):
        self.screen_center_y+=2
        self.center_y -= 1


        if self.center_y < self.screen_center_y-30:

            self.reset_pos()

    def update_animation(self, seconds):
        if seconds - self.aux_segundos > 0.1:
            if (self.animacion == 2):
                self.animacion = 0
            if (self.animacion == 0):
                self.texture = arcade.load_texture(
                    ".." + os.path.sep + "assets" + os.path.sep + "sprites" + os.path.sep + "tiburon1.png")
            elif (self.animacion == 1):
                self.texture = arcade.load_texture(
                    ".." + os.path.sep + "assets" + os.path.sep + "sprites" + os.path.sep + "tiburon3.png")
            self.animacion += 1
            self.aux_segundos = seconds

class barco_pesquero(arcade.Sprite):
    def __init__(self, filename, sprite_scaling, ):
        super().__init__(filename, sprite_scaling)
        self.vida = 5
        self.aux_segundos = 0
        self.animacion = 0
    def reset_pos(self):
        self.center_y += 2
        self.center_x = random.randrange(700, 750)

    def update(self):
        self.center_x -= 0.8
        self.center_y += 2
        if self.left < -150:
            self.reset_pos()
    def update_animation(self, seconds):
        if seconds - self.aux_segundos > 0.1:
            if (self.animacion == 2):
                self.animacion = 0
            if (self.animacion == 0):
                self.texture = arcade.load_texture(
                    ".." + os.path.sep + "assets" + os.path.sep + "sprites" + os.path.sep + "barco_pesca_1.png")
            elif (self.animacion == 1):
                self.texture = arcade.load_texture(
                    ".." + os.path.sep + "assets" + os.path.sep + "sprites" + os.path.sep + "barco_pesca_2.png")
            self.animacion += 1
            self.aux_segundos = seconds



class InicioView(arcade.View):
    def __init__(self,nivel_superado):
        super().__init__()
        self.nivel_superado=nivel_superado
        if self.nivel_superado==1:
            self.texture = arcade.load_texture(".."+os.path.sep+"assets"+os.path.sep+"images"+os.path.sep+"Menu_Inicio.png ")
        else:
            self.texture = arcade.load_texture(".." + os.path.sep + "assets" + os.path.sep + "images" + os.path.sep + "Menu_Victoria_Alternativo.png ")
        arcade.set_viewport(0, SCREEN_HEIGHT - 1, 0, SCREEN_WIDTH - 1)

    def on_draw(self):
        arcade.start_render()
        self.texture.draw_sized(SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2, SCREEN_HEIGHT, SCREEN_WIDTH)

    def on_key_press(self, key, _modifiers):

        if key == arcade.key.SPACE:
            if self.nivel_superado==1:
                Historia = MenuHistoria()
                self.window.show_view(Historia)
            else:
                game_view = MyGame(SCREEN_HEIGHT, SCREEN_WIDTH, "Sprite Example")
                game_view.setup(self.nivel_superado)
                self.window.show_view(game_view)
        elif key == arcade.key.C:
            Instruction = InstructionView(self, screen_center_y=0)
            self.window.show_view(Instruction)

class MenuHistoria(arcade.View):
    def __init__(self):
        super().__init__()
        self.contador=1
        self.texture1 = arcade.load_texture(".." + os.path.sep + "assets" + os.path.sep + "images" + os.path.sep + "Menu_Historia1.png ")
        self.texture2 = arcade.load_texture(".." + os.path.sep + "assets" + os.path.sep + "images" + os.path.sep + "Menu_Historia2.png ")
        self.texture3 = arcade.load_texture(".." + os.path.sep + "assets" + os.path.sep + "images" + os.path.sep + "Menu_Historia3.png ")
        self.texture4 = arcade.load_texture(".." + os.path.sep + "assets" + os.path.sep + "images" + os.path.sep + "Menu_Historia4.png ")
    def on_draw(self):
        arcade.start_render()
        if self.contador==1:
            self.texture1.draw_sized(SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2, SCREEN_HEIGHT, SCREEN_WIDTH)
        elif self.contador==2:
            self.texture2.draw_sized(SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2, SCREEN_HEIGHT, SCREEN_WIDTH)
        elif self.contador==3:
            self.texture3.draw_sized(SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2, SCREEN_HEIGHT, SCREEN_WIDTH)
        elif self.contador==4:
            self.texture4.draw_sized(SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2, SCREEN_HEIGHT, SCREEN_WIDTH)
    def on_key_press(self, key, _modifiers):

        if key == arcade.key.C:
            if self.contador==4:
                game_view = MyGame(SCREEN_HEIGHT, SCREEN_WIDTH, "Sprite Example")
                game_view.setup(1)
                self.window.show_view(game_view)
            else:
                self.contador+=1

class MyGame(arcade.View):
    def __init__(self, Width, heiht, title):
        """Initializer"""
        super().__init__()
        self.player_list = None
        self.bullet_list = None
        self.coin_list = None
        self.obstaculo_list = None
        self.ship = None
        self.enemigo_list = None
        self.ataques_list = None
        self.background_list = None
        self.tiburon_sprite_list = None
        self.barco_pesquero_list = None
        self.arpon_list = None
        self.tile_map = None
        self.score = 0
        self.layer = 1
        self.my_map = None
        self.end_of_map = 0
        self.frame_count = 0
        self.screen_center_x = 0
        self.screen_center_y = 0
        self.total_time = 0
        self.aux=1
        self.aux_texto_score = 750
        self.coste_escudo = 5
        self.desactivar_disparo = False
        self.contador_enemigos=0
        arcade.set_background_color(arcade.color.AMAZON)
        self.perder_vida=arcade.sound.load_sound(".."+os.path.sep+"assets"+os.path.sep+"sounds"+os.path.sep+"Perder_vida.mp3")
        self.disparo_Barco = arcade.sound.load_sound(".." + os.path.sep + "assets" + os.path.sep + "sounds" + os.path.sep + "Disparo_flechas.mp3")
        self.muerte_enemigo = arcade.sound.load_sound(":resources:sounds"+ os.path.sep + "explosion2.wav")
        self.Victoria = arcade.sound.load_sound(".." + os.path.sep + "assets" + os.path.sep + "sounds" + os.path.sep + "Sonido_victoria.mp3")
    def setup(self,nivel_superado):
        self.nivel_superado=nivel_superado
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemigo_list = arcade.SpriteList()
        self.ataques_list = arcade.SpriteList()
        self.ship = player(".."+os.path.sep+"assets"+os.path.sep+"sprites"+os.path.sep+"Barco - forma 1_3.png", SPRITE_SCALING_PLAYER)
        self.ship.center_x = 100
        self.ship.center_y = 80
        self.player_list.append(self.ship)
        self.tiburon_sprite_list = arcade.SpriteList()
        self.barco_pesquero_list = arcade.SpriteList()
        self.arpon_list = arcade.SpriteList()
        if self.nivel_superado==1:
            map_name = f".."+os.path.sep+"assets"+os.path.sep+"tilemaps"+os.path.sep+"Mapa de introducción"+os.path.sep+"mapa_intro_v4.json"
            layer_options = {Background_layer: {"use_spatial_hash": False}, }
            self.my_map = arcade.tilemap.load_tilemap(map_name, 1.9, layer_options)
            self.end_of_map = 800

            self.scene = arcade.Scene.from_tilemap(self.my_map)
            self.camera = arcade.Camera(SCREEN_HEIGHT, SCREEN_WIDTH)
            self.camera_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.pan_camera_to_user()

            for i in range(3):
                enemigo2 = tiburon(".."+os.path.sep+"assets"+os.path.sep+"sprites"+os.path.sep+"tiburon1.png", SPRITE_TIBURON)
                enemigo2.center_y = 900
                enemigo2.center_x = random.randrange(70, 530)
                self.tiburon_sprite_list.append(enemigo2)

            for i in range(3):
                enemigo3 = barco_pesquero(".."+os.path.sep+"assets"+os.path.sep+"sprites"+os.path.sep+"barco_pesca_1.png", SPRITE_BARCO_PESQUERO)
                enemigo3.center_x = 700
                enemigo3.center_y = random.randrange(500, 700)
                self.barco_pesquero_list.append(enemigo3)
        if self.nivel_superado==2:


            map_name = f".."+os.path.sep+"assets"+os.path.sep+"tilemaps"+os.path.sep+"Mapa"+os.path.sep+"mapaV1.json"
            layer_options = {Background_layer: {"use_spatial_hash": False}, }
            self.my_map = arcade.tilemap.load_tilemap(map_name, 1.9, layer_options)
            self.end_of_map = 800
            self.ship.vida=5
            self.ship.nivel=2
            self.scene = arcade.Scene.from_tilemap(self.my_map)
            self.camera = arcade.Camera(SCREEN_HEIGHT, SCREEN_WIDTH)
            self.camera_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.pan_camera_to_user()

            for i in range(3):
                enemigo2 = tiburon(".."+os.path.sep+"assets"+os.path.sep+"sprites"+os.path.sep+"tiburon1.png", SPRITE_TIBURON)
                enemigo2.center_y = 900
                enemigo2.center_x = random.randrange(70, 530)
                self.tiburon_sprite_list.append(enemigo2)

            for i in range(3):
                enemigo3 = barco_pesquero(".."+os.path.sep+"assets"+os.path.sep+"sprites"+os.path.sep+"barco_pesca_1.png", SPRITE_BARCO_PESQUERO)
                enemigo3.center_x = 700
                enemigo3.center_y = random.randrange(500, 700)
                self.barco_pesquero_list.append(enemigo3)

    def on_resize(self, width, height):
        self.camera.resize(width, height)
        self.camera_gui.resize(width, height)

    def on_draw(self):
        self.clear()
        self.scene.draw()
        self.camera.use()
        self.camera_gui.use
        self.coin_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()
        self.enemigo_list.draw()
        self.ataques_list.draw()
        self.tiburon_sprite_list.draw()
        self.barco_pesquero_list.draw()
        self.arpon_list.draw()

        self.sprite = arcade.load_texture(".." + os.path.sep + "assets" + os.path.sep + "sprites" + os.path.sep + "Sprite_vidas.png")
        self.sprite.draw_sized(36, self.aux_texto_score + 10, 34, 34)
        arcade.draw_text('      : ' + str(self.ship.vida), 15.0, self.aux_texto_score, arcade.color.RED, 20, 180, 'left')

        self.sprite = arcade.load_texture(".." + os.path.sep + "assets" + os.path.sep + "sprites" + os.path.sep + "score.png")
        self.sprite.draw_sized(520, self.aux_texto_score + 10, 34, 34)
        arcade.draw_text(' : ' + str(self.score), 470.0, self.aux_texto_score, arcade.color.RED, 20, 180, 'center')
        
        arcade.draw_text('Escudo : ' + str(self.coste_escudo), 450, self.aux_texto_score - 30,
                         arcade.color.RED, 20, 180, 'left')

        self.sprite = arcade.load_texture(".." + os.path.sep + "assets" + os.path.sep + "sprites" + os.path.sep + "Pez_contaminado_2.png")
        self.sprite.draw_sized(36, self.aux_texto_score-27, 80, 65)
        arcade.draw_text('      : ' + str(self.contador_enemigos), 15.0, self.aux_texto_score - 30, arcade.color.RED, 20, 180, 'left')
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.N and self.score >= self.coste_escudo:
            self.ship.escudo = True
            self.desactivar_disparo = True
            self.score -= self.coste_escudo
            self.coste_escudo += 2

        elif key == arcade.key.SPACE and self.desactivar_disparo == False:
            if self.score <= 20:
                bullet = arcade.Sprite(".."+os.path.sep+"assets"+os.path.sep+"sprites"+os.path.sep+"bullet3.png", SPRITE_SCALING_BULLET)
                start_x = self.ship.center_x
                start_y = self.ship.center_y
                bullet.center_x = start_x
                bullet.center_y = start_y

                bullet.change_y = BULLET_SPEED
                self.bullet_list.append(bullet)
            else:
                bullet1 = arcade.Sprite(".."+os.path.sep+"assets"+os.path.sep+"sprites"+os.path.sep+"bullet3.png", SPRITE_SCALING_BULLET)
                bullet2 = arcade.Sprite(".."+os.path.sep+"assets"+os.path.sep+"sprites"+os.path.sep+"bullet3.png", SPRITE_SCALING_BULLET)
                # Position the bullet at the player's current location
                start_x1 = self.ship.center_x - 20
                start_y1 = self.ship.center_y - 20
                start_x2 = self.ship.center_x + 20
                start_y2 = self.ship.center_y + 20
                bullet1.center_x = start_x1
                bullet1.center_y = start_y1
                bullet2.center_x = start_x2
                bullet2.center_y = start_y2
                bullet1.change_y = BULLET_SPEED
                bullet2.change_y = BULLET_SPEED
                self.bullet_list.append(bullet1)
                self.bullet_list.append(bullet2)
            arcade.sound.play_sound(self.disparo_Barco, 0.01)
        if key == arcade.key.W:
            self.ship.speed = MOVEMENT_SPEED + 3
            self.ship.up = True
        elif key == arcade.key.S:
            if self.ship.limite == True:
                self.ship.speed = -MOVEMENT_SPEED
            self.ship.up = True
        elif key == arcade.key.A:
            self.ship.change_angle = -an_vel
        elif key == arcade.key.D:
            self.ship.change_angle = an_vel
        elif key == arcade.key.ESCAPE:
            media_player.pause()
            pause = PauseView(self, self.screen_center_y)
            self.window.show_view(pause)
        self.ship.limite = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.ship.speed = 0
            self.ship.up = False
        elif key == arcade.key.A or key == arcade.key.D:
            self.ship.change_angle = 0
        elif key == arcade.key.N:
            self.ship.escudo = False
            self.desactivar_disparo = False

    def disparo_enemigo(self):

        for enemigo in self.enemigo_list:

            if type(enemigo) == pez:
                if enemigo.control >= 100:
                    ataque = ataque_pez(".."+os.path.sep+"assets"+os.path.sep+"sprites"+os.path.sep+"Disparo_burbuja.png", SPRITE_SCALING_BULLET)
                    start_x = enemigo.center_x
                    start_y = enemigo.center_y
                    ataque.center_x = start_x
                    ataque.center_y = start_y
                    self.ataques_list.append(ataque)
                    enemigo.control = 0

    def pan_camera_to_user(self, panning_fraction: float = 0.1):
        self.screen_center_y += 2
        user_centered = self.screen_center_x, self.screen_center_y

        self.camera.move_to(user_centered, panning_fraction)

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.total_time += delta_time
        self.seconds = int(self.total_time) % 60
        # Call update on all sprites
        self.bullet_list.update()
        self.player_list.update()
        self.ship.update_animation(self.seconds)
        self.enemigo_list.update()
        self.disparo_enemigo()
        self.tiburon_sprite_list.update_animation(self.seconds)
        self.barco_pesquero_list.update_animation(self.seconds)
        self.enemigo_list.update_animation(self.seconds)
        self.ataques_list.update()
        self.tiburon_sprite_list.update()
        self.barco_pesquero_list.update()
        self.aux_texto_score += 2
        self.frame_count += 1
        self.pan_camera_to_user(panning_fraction=0.12)
        if media_player.time>213:
            media_player.seek(20)
            media_player.play

        for barco in self.barco_pesquero_list:
            start_x = barco.center_x
            start_y = barco.center_y
            dest_x = self.ship.center_x
            dest_y = self.ship.center_y
            x_diff = dest_x - start_x
            y_diff = (dest_y+40) - start_y
            angle = math.atan2(y_diff, x_diff)
            if self.frame_count % 100 == 0:
                arpon = arcade.Sprite(".."+os.path.sep+"assets"+os.path.sep+"sprites"+os.path.sep+"Disparo_fecha.png")
                arpon.center_x = start_x
                arpon.center_y = start_y
                arpon.angle = math.degrees(angle)
                arpon.change_x = math.cos(angle) * VEL_ARPON
                arpon.change_y = math.sin(angle) * VEL_ARPON

                self.arpon_list.append(arpon)
        for arpon in self.arpon_list:
            if arpon.top < 0:
                arpon.remove_from_sprite_lists()

        self.arpon_list.update()
        for player in self.player_list:
            if player.vida <= 0:
                player.remove_from_sprite_lists()
                GameOver = GameOverView(self, self.screen_center_y,self.nivel_superado)
                media_player.pause()
                self.window.show_view(GameOver)
            hit_list = arcade.check_for_collision_with_list(player, self.scene[Obtaculos_layer])
            hit_list_daño = arcade.check_for_collision_with_list(player, self.scene[Piedras_layer])
            for piedra in hit_list_daño:
                piedra.remove_from_sprite_lists()
                if self.ship.escudo == False:
                    player.vida -= 1
                    arcade.sound.play_sound(self.perder_vida, 0.1)
            for coin in hit_list:
                coin.remove_from_sprite_lists()
                self.score += 1
            hit_list = arcade.check_for_collision_with_list(player, self.tiburon_sprite_list)
            for tiburon in hit_list:
                if self.ship.escudo == False:
                    player.vida -= 1
                    arcade.sound.play_sound(self.perder_vida, 0.1)
                    tiburon.screen_center_y = 1000
                    tiburon.center_y += self.screen_center_y + 350
                    tiburon.center_x = random.randrange(70, 530)



        if self.ship.escudo == True:

            for ataque in self.ataques_list:
                hit_list = arcade.check_for_collision_with_list(ataque, self.player_list)
                if len(hit_list) > 0:
                    self.ship.vida = self.ship.vida

        else:

            for ataque in self.ataques_list:
                hit_list = arcade.check_for_collision_with_list(ataque, self.player_list)
                if len(hit_list) > 0:
                    self.ship.vida -= 1
                    arcade.sound.play_sound(self.perder_vida, 0.1)
                    ataque.remove_from_sprite_lists()
            for arpon in self.arpon_list:
                hit_list = arcade.check_for_collision_with_list(arpon, self.player_list)
                if len(hit_list) > 0:
                    self.ship.vida -= 1
                    arcade.sound.play_sound(self.perder_vida, 0.1)
                    arpon.remove_from_sprite_lists()
        for bullet in self.bullet_list:
            hit_list_enemigo = arcade.check_for_collision_with_list(bullet, self.enemigo_list)
            hit_list_enemigo2 = arcade.check_for_collision_with_list(bullet, self.tiburon_sprite_list)
            hit_list_enemigo3 = arcade.check_for_collision_with_list(bullet, self.barco_pesquero_list)
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
            for enemigo in hit_list_enemigo:
                enemigo.vida -= 1
                if enemigo.vida <= 0:
                    arcade.sound.play_sound(self.muerte_enemigo, 0.1)
                    enemigo.screen_center_y = 1000
                    enemigo.center_y =self.screen_center_y+800
                    enemigo.center_x = random.randrange(70, 400)
                    bullet.remove_from_sprite_lists()
                    self.contador_enemigos+=1

                    self.score += 1
            for tiburon in hit_list_enemigo2:
                tiburon.vida -= 1
                arcade.sound.play_sound(self.muerte_enemigo, 0.1)
                if tiburon.vida <= 0:

                    tiburon.center_y = self.screen_center_y + 900
                    tiburon.center_x = random.randrange(70, 530)
                    bullet.remove_from_sprite_lists()
                    self.contador_enemigos += 1
                    self.score += 1

            for barco_pesquero in hit_list_enemigo3:
                barco_pesquero.vida -= 1
                if barco_pesquero.vida <= 0:
                    arcade.sound.play_sound(self.muerte_enemigo, 0.1)
                    barco_pesquero.center_y = random.randrange(barco_pesquero.center_y-200,barco_pesquero.center_y+100)
                    barco_pesquero.center_x = random.randrange(700, 750)
                    bullet.remove_from_sprite_lists()
                    self.contador_enemigos += 1
                    self.score += 1

        if self.screen_center_y>=8800:
            GameOver = GameOverView(self, self.screen_center_y,self.nivel_superado)
            media_player.pause()
            self.window.show_view(GameOver)
        if self.contador_enemigos>=50 and self.nivel_superado==1:
            self.contador_enemigos=0
            self.nivel_superado=2

            Menu = InicioView(self.nivel_superado)
            self.window.show_view(Menu)
        if self.contador_enemigos>=20 and self.nivel_superado==2 and self.aux==1:
            for i  in range(1):
                enemigo = pez( ".." + os.path.sep + "assets" + os.path.sep + "sprites" + os.path.sep + "Pez_contaminado_1.png", 0.4)
                enemigo.center_x = self.screen_center_x+400
                enemigo.center_y = self.screen_center_y+800
                enemigo.start_x = enemigo.center_x
                enemigo.start_y = enemigo.center_y
                enemigo.vida=5
                self.barco_pesquero_list[0].remove_from_sprite_lists()
                self.enemigo_list.append(enemigo)
                self.aux=0
        if self.contador_enemigos >= 50 and self.nivel_superado == 2:
            media_player.pause()
            arcade.sound.play_sound(self.Victoria, 0.3)
            Menu = Pantalla_Victoria(self, self.screen_center_y)
            self.window.show_view(Menu)
class InstructionView(arcade.View):
    def __init__(self, game_view, screen_center_y):
        super().__init__()
        self.game_view = game_view
        self.texture = arcade.load_texture(".."+os.path.sep+"assets"+os.path.sep+"images"+os.path.sep+"Lista_Controles.png ")
        self.screen_center_y = screen_center_y

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        self.texture.draw_sized(SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2 + self.screen_center_y, SCREEN_HEIGHT, SCREEN_WIDTH)

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)


class PauseView(arcade.View):
    def __init__(self, game_view, screen_center_y):
        super().__init__()
        self.game_view = game_view
        self.texture = arcade.load_texture(".."+os.path.sep+"assets"+os.path.sep+"images"+os.path.sep+"Menu_Pausa.png ")
        self.ui_manager = arcade.gui.UIManager(self.window)
        self.screen_center_y = screen_center_y

    def on_show_view(self):

        self.ui_manager.enable()

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()
        self.texture.draw_sized(SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2 + self.screen_center_y, SCREEN_HEIGHT, SCREEN_WIDTH)

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)
            media_player.play()
        elif key == arcade.key.B:
            media_player.play()
            Menu = InicioView()
            self.window.show_view(Menu)
        elif key == arcade.key.S:
            sonido = SonidoView(self, self.screen_center_y)
            self.window.show_view(sonido)
        elif key == arcade.key.C:
            Instruction = InstructionView(self, self.screen_center_y)
            self.window.show_view(Instruction)

class Pantalla_Victoria(arcade.View):
    def __init__(self, game_view, screen_center_y):
        super().__init__()
        self.game_view = game_view
        self.texture = arcade.load_texture(
            ".." + os.path.sep + "assets" + os.path.sep + "images" + os.path.sep + "Menu_Victoria.png")

        self.screen_center_y = screen_center_y
    def on_draw(self):
            self.clear()
            self.texture.draw_sized(SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2 + self.screen_center_y, SCREEN_HEIGHT,
                                    SCREEN_WIDTH)
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:  # resume game
            media_player.play()
            Menu = InicioView(1)
            self.window.show_view(Menu)
class GameOverView(arcade.View):
    def __init__(self, game_view, screen_center_y,nivel_superado):
        super().__init__()
        self.game_view = game_view
        self.texture = arcade.load_texture(".."+os.path.sep+"assets"+os.path.sep+"images"+os.path.sep+"Game_Over(provisional).png")
        self.screen_center_y = screen_center_y
        self.nivel_superado=nivel_superado
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        self.texture.draw_sized(SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2 + self.screen_center_y, SCREEN_HEIGHT, SCREEN_WIDTH)


    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:  # resume game
            media_player.play()
            Menu = InicioView(self.nivel_superado)
            self.window.show_view(Menu)

def main():
    Window = arcade.Window(SCREEN_HEIGHT, SCREEN_WIDTH, "Sea Defender")
    start_View = InicioView(nivel_superado)
    Window.show_view(start_View)
    arcade.run()


if __name__ == "__main__":
    main()



