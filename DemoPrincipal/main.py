'''
Trabajo de Estructuras de Datos
=========
'''

from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Mesh
from kivy.graphics import Color
from functools import partial
from math import cos, sin, pi, floor
from timeit import default_timer as timer
import random
import math
from LayeredRangeTree import LayeredRangeTree 


class TouchInput(Widget):

    def on_touch_down(self, touch):        
        if self.app.pos1 is None:
            self.app.pos1 = touch.pos
            self.app.textIni.text = str(touch.pos)
        elif self.app.pos2 is None and (self.app.pos1[0] != touch.pos[0] and self.app.pos1[1] != touch.pos[1]):
            self.app.pos2 = touch.pos
            self.app.textFin.text = str(touch.pos)
        #print(touch.pos)
        #print(touch.button)
    
class TrabajoEstructurasDatosApp(App):

    def search(self, event):
        
        if self.pos1 is None or self.pos2 is None:
            return

        points = self.tree.totalSearch( [self.pos1[0], self.pos1[1]], [self.pos2[0], self.pos2[1]] ) 
        
        for widget in self.widBusqueda:
            self.root.remove_widget(widget)

        self.widBusqueda.clear()
        
        for index in range(20):
            wid = TouchInput(id='widBusqueda'+str(index))
            wid.app = self
            wid.height = Window.height
            wid.width = Window.width
            step = math.floor(len(points)/20)
            with wid.canvas:
                self.points = self.build_mesh_query(points[index*step:(index+1)*step])
            self.widBusqueda.append(wid)
            
        for index in range(20):
            wid = self.widBusqueda[index]
            with wid.canvas.before:
                    Color(1.0, 0.0, 0.0, 1.0)
                    
            self.root.add_widget(self.widBusqueda[index])

        
        self.pos1 = None
        self.pos2 = None

    def callback(self, event):
        self.lista = []
        self.draw_Points()
        print("Antes de la creación")
        self.tree = LayeredRangeTree( self.lista )
        print("Antes de la Búsqueda")
        

    def build_mesh(self):
        vertices = []
        indices  = []

        for count in range( floor(int(self.text.text)/20) ):
            x = random.random() * Window.width
            y = random.random() * Window.height - 50
            vertices.extend( [x, y, 0, 0] )
            self.lista.append( [x, y] )
            indices.append(count)
        return Mesh( vertices=vertices, indices=indices )

    def build_mesh_query(self, points):
        vertices = []
        indices  = []
        count = 0
        for point in points :
            vertices.extend( [point[0], point[1], 0, 0] )
            indices.append(count)
            count += 1
        return Mesh( vertices=vertices, indices=indices )

    def draw_Points(self):

        if not self.text.text.isnumeric():
            view = ModalView(size_hint=(None, None), size=(400, 200))
            view.add_widget(Label(text='Por favor ingrese una cantidad entera'))
            view.open()
            return
        else:
            cantidad = int(self.text.text)
            if cantidad > 275000:
                view = ModalView(size_hint=(None, None), size=(400, 200))
                view.add_widget(Label(text='La cantidad de puntos debe de ser menor a 275000'))
                view.open()
                return
        
        for widget in self.wids:
            self.root.remove_widget(widget)

        self.wids.clear()
        
        for index in range(20):
            wid = TouchInput(id='wid'+str(index))
            wid.app = self
            wid.height = Window.height
            wid.width = Window.width
            with wid.canvas:
                self.points = self.build_mesh()
            self.wids.append(wid)
            
        for index in range(20):
            wid = self.wids[index]
            with wid.canvas.before:
                    Color(1.0, 1.0, 1.0, 1.0)
                    
            self.root.add_widget(self.wids[index])

        

    def build(self):

        #Window.bind(on_touch_down=self.on_touch_down)
        
        self.wids = []
        
        Window.maximize()
        
        self.title = "Trabajo de Estructura de Datos"
        
        layout = BoxLayout(size_hint=(1, None), height=40)

        self.text = TextInput()
        buttonGraph = Button(text='Graficar aleatorio')
        buttonSearch = Button(text='Buscar')
        layout.add_widget(buttonGraph)
        layout.add_widget(self.text)
        layout.add_widget(buttonSearch)
        self.textIni = TextInput(readonly= True)
        self.textFin = TextInput(readonly= True)
        layout.add_widget(self.textIni)
        layout.add_widget(self.textFin)
        
        buttonGraph.bind(on_press=self.callback)
        buttonSearch.bind(on_press=self.search)

        pointsLayout = BoxLayout()
        
        self.root = BoxLayout(orientation = 'vertical')
       
        self.root.add_widget(layout)
        self.root.add_widget(pointsLayout)

        self.tree = None

        self.lista = []

        self.pos1 = None
        self.pos2 = None

        self.widBusqueda = []

##        self.draw_Points()

        return self.root


if __name__ == '__main__':
    TrabajoEstructurasDatosApp().run()
