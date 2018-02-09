from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
from kivy.uix.modalview import ModalView

from kivy.app import App
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.graphics.vertex_instructions import Triangle
from LayeredRangeTree import LayeredRangeTree
from LayeredRangeTree import InternalNode
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.core.text import Label as CoreLabel
from kivy.uix.label import Label
import math

class GraphicalNode:

    def __init__( self, dad, canvas, node, x, y, level, w1, w2, h, dy ):
        self.dad = dad
        self.canvas = canvas
        self.node = node
        self.x = x
        self.y = y
        self.level = level
        self.w1 = w1
        self.w2 = w2
        self.size = [40,40]
        self.h = y - h * dy

    def getTriangle(self):
        self.canvas.add(Color(1, 0, 0, 0.5))
        self.canvas.add( Line( points = [ self.x+self.size[0]/2, self.y+self.size[0]*2, self.w1-self.size[0]/4, self.h , self.w2+self.size[0], self.h, self.x+self.size[0]/2, self.y+self.size[0]*2 ] ) )
    
    def draw( self ):

        #------------------- Draw Line -------------------#
        self.canvas.add(Color(1, 0.8, 0.1, 0.5))
        if not self.dad is None:
            self.canvas.add( Line(points=[self.x+ (self.size[0]/2) , self.y+ (self.size[0]/2), self.dad.x+ (self.size[0]/2), self.dad.y+ (self.size[0]/2)], width=1) )
        self.canvas.ask_update()
        
        #------------------- Draw a Node -------------------#
        if self.node.isLeaf():
            self.canvas.add(Color(0.4, 1, 0.4, 1))
            self.canvas.add( Rectangle( pos = [self.x,self.y], size = self.size ) )
        else:
            self.canvas.add(Color(1, 0.8, 0.1, 1))
            self.canvas.add( Ellipse( pos = [self.x,self.y], size = self.size ) )
        self.canvas.ask_update()
        
        #------------------- Draw key's Text-------------------#
        pos = [self.x, self.y]
        label = CoreLabel(text=str(self.node.k), font_size=8)
        label.refresh()
        text = label.texture
        self.canvas.add(Color(0, 0, 0, 1))
        pos = list(pos[i] + (self.size[i] - text.size[i]) / 2 for i in range(2))
        self.canvas.add(Rectangle(size=text.size, pos=pos, texture=text))
        self.canvas.ask_update()

        #------------------- Draw key's Factor-------------------#
        if not self.node.isLeaf():
            pos = [self.x + self.size[0]*0.75, self.y+5]
            label = CoreLabel(text=str(self.node.factor), font_size=8)
            label.refresh()
            text = label.texture
            self.canvas.add(Color(0, 0, 1, 1))
            pos = list(pos[i] + (self.size[i] - text.size[i]) / 2 for i in range(2))
            self.canvas.add(Rectangle(size=text.size, pos=pos, texture=text))
            self.canvas.ask_update()
        

class TreeWidget(Widget):

    r = NumericProperty(0)

    def __init__(self, tree, dictionary, **args):

        self.tree = tree

        self.dictionary = dictionary

        super(TreeWidget, self).__init__(**args)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.bind( r = self.redraw )
        self.bind( pos = self.redraw )
        self.bind( size = self.redraw )
        self.size = [ 250, 250 ]
        self.pos  = [ 100, 100 ]

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def redraw(self, *args):

        self.canvas.clear()

        x = 5000
        y = 1000
        dx = 100
        dy = 80
        h = self.tree.getHeight()
        w = pow( 2, h-1 )*dx
        w1 = x-w/2
        w2 = x+w/2
        
        self.canvas.add(Color(self.r, 1, 1, 1))
        
        Q = []

        Q.append(GraphicalNode( None, self.canvas, self.tree.root , x, y, 1, w1, w2, h, dy ))

        while len(Q) > 0:
            node = Q.pop()
            node.draw()
            self.dictionary[str(node.node.k) + "_" + str(node.node.isLeaf())] = node
            if not node.node.child[0] is None:
                if not node.node.child[0].isLeaf():                    
                    Q.append( GraphicalNode( node, self.canvas, node.node.child[0], math.floor(node.x+node.w1)/2, node.y-dy, node.level + 1, node.w1, node.x, self.tree.__getHeight__(node.node.child[0]), dy ) )
                else:
                    child = GraphicalNode( node, self.canvas, node.node.child[0], math.floor(node.x+node.w1)/2, node.y-dy, node.level + 1, node.w1, node.x,self.tree.__getHeight__(node.node.child[0]), dy )
                    child.draw()
                    self.dictionary[str(node.node.child[0].k) + "_" + str(node.node.child[0].isLeaf())] = child
            if not node.node.child[1] is None:
                if not node.node.child[1].isLeaf():
                    Q.append( GraphicalNode( node, self.canvas, node.node.child[1], math.floor(node.x+node.w2)/2, node.y-dy, node.level + 1, node.x, node.w2, self.tree.__getHeight__(node.node.child[1]), dy ) )
                else:
                    child = GraphicalNode( node, self.canvas, node.node.child[1], math.floor(node.x+node.w2)/2, node.y-dy, node.level + 1, node.x, node.w2,self.tree.__getHeight__(node.node.child[1]), dy )
                    child.draw()
                    self.dictionary[str(node.node.child[1].k) + "_" + str(node.node.child[1].isLeaf())] = child
            
    #def on_touch_down( self, touch ):
     
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'q':
            self.viewPopup = ModalView(size_hint=(None, None), size=(100, 100))
            boxLayout =  BoxLayout(orientation='vertical', size_hint_y=None, size_hint_x=None, height=100, width=100)
            self.viewPopup.add_widget(boxLayout)
            boxLayout.add_widget(TextInput())
            boxLayout.add_widget(TextInput())
            boxLayout.add_widget(Button(text="Agregar"))
            self.viewPopup.open()
        return True

class TreeDrawerApp(App):

    def build(self):

        self.dictionary = {}

        self.tree = LayeredRangeTree()

        #list = [4]#4, 6, 2, 12, 13, 40, 5, 14, 204,1,8,10,80,95,2,3,5,111,213,1111,3,34,37,38,76,-3,-5,-8,-10]
        list = [2,10,17,1,5,5,13,100,9,1,2]

        for n in list:
            self.tree.insert(n,0)

        Window.maximize()
        Window.clearcolor = (1, 1, 1, 1)
        self.title = "Trabajo de Estructura de Datos - Range Tree 1D"
        

        root = BoxLayout(orientation = 'vertical',size_hint=(1, None), height = Window.height+110)
        panel = BoxLayout(orientation = 'horizontal', height=40,size_hint=(1, None))
        self.textX = TextInput()
        panel.add_widget(self.textX)
        btnInsertar = Button(text='Insertar')
        panel.add_widget(btnInsertar)
        btnInsertar.bind(on_press=self.insertarEnArbol)
        self.textX1 = TextInput()
        self.textX2 = TextInput()
        btnBuscar = Button(text = 'Buscar')
        btnBuscar.bind(on_press=self.buscarEnArbol)
        panel.add_widget(self.textX1)
        panel.add_widget(self.textX2)
        panel.add_widget(btnBuscar)
        
        scrollView = ScrollView(size=(Window.width, Window.height), do_scroll_x = True, do_scroll_y = True)
        box = BoxLayout(orientation='vertical', size_hint_y=None, height=1100, size_hint_x=None, width=10000)
        root.add_widget(panel)
        self.graphTree = TreeWidget(self.tree, self.dictionary)
        box.add_widget( self.graphTree )
        scrollView.add_widget(box)
        scrollView.scroll_x = 0.5
        root.add_widget(scrollView)
        
        return root

    def insertarEnArbol(self, args):

        if not self.textX.text.isnumeric():
            view = ModalView(size_hint=(None, None), size=(400, 200))
            view.add_widget(Label(text='Por favor ingrese números válidos'))
            view.open()
        else:
            self.tree.insert( int(self.textX.text),0)
            self.graphTree.redraw()
        pass

    def buscarEnArbol(self, args):

        if not self.textX1.text.isnumeric() or not self.textX2.text.isnumeric():
            view = ModalView(size_hint=(None, None), size=(400, 200))
            view.add_widget(Label(text='Por favor ingrese números válidos'))
            view.open()
        else:
            S = self.tree.searchTrees( int(self.textX1.text),int(self.textX2.text))
            self.graphTree.redraw()
            for node in S:
                self.dictionary[str(node.k) + "_" + str(node.isLeaf())].getTriangle()
        pass

if __name__ == '__main__':
    TreeDrawerApp().run()
