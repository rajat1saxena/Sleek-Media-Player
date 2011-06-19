import gst
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade

class guibuild:
    def on_message(self,bus,message):
        if message.type==gst.MESSAGE_EOS:
            self.myplay.set_state(gst.STATE_NULL)
        elif message.type==gst.MESSAGE_ERROR:
            self.myplay.set_state(gst.STATE_NULL)
            (err,debug)=message.parse_error()
            print("Error: %s"%err,debug)
    def on_play(self,widget):
        self.mediafile=self.open.get_filename()
        self.mediafile="file://"+self.mediafile
        print(self.mediafile)
        self.myplay.set_property("uri",self.mediafile)
        self.myplay.set_state(gst.STATE_PLAYING)
    def on_stop(self,widget):
        self.myplay.set_state(gst.STATE_NULL)
    def on_pause(self,widget):
        self.myplay.set_state(gst.STATE_PAUSED)
    def __init__(self):
        self.filename="/home/rajat/ap/interface.glade"
        self.builder=gtk.Builder()
        self.builder.add_from_file(self.filename)

        #getting objects
        self.win=self.builder.get_object("mainwin")
        self.hbox=self.builder.get_object("hbox")
        self.play=self.builder.get_object("play")
        self.pause=self.builder.get_object("pause")
        self.stop=self.builder.get_object("stop")
        self.open=self.builder.get_object("open")

        #connecting objects with callback functions
        self.win.connect("destroy",gtk.main_quit)
        self.play.connect("clicked",self.on_play)
        self.pause.connect("clicked",self.on_pause)
        self.stop.connect("clicked",self.on_stop)

        #setting filechooser button's properties
        self.open.set_current_folder("/home")

        #creating gst playbin to play media file
        self.myplay=gst.element_factory_make("playbin","Rajat Player")
        #self.mediafile="file:///home/rajat/peat.mp3"
        #self.myplay.set_property("uri",self.mediafile)
        self.bus=self.myplay.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message",self.on_message)

        #showing the main window
        self.win.show_all()
    
if __name__=="__main__":
    mybuild=guibuild()
    gtk.main()
    
