# guibuild.py
# an ultra simple audio player for Ubuntu
# Copyright (C) 2011 Rajat Saxena
#
# rajat.saxena.work@gmail.com
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
        self.win.set_title(self.mediafile)
        self.myplay.set_property("uri",self.mediafile)
        self.myplay.set_state(gst.STATE_PLAYING)
    def on_stop(self,widget):
        self.myplay.set_state(gst.STATE_NULL)
    def on_pause(self,widget):
        self.myplay.set_state(gst.STATE_PAUSED)
    def __init__(self):
        self.filename="./interface.glade"
        self.builder=gtk.Builder()
        self.builder.add_from_file(self.filename)

        #getting objects
        self.win=self.builder.get_object("mainwin")
        self.hbox=self.builder.get_object("hbox")
        self.play=self.builder.get_object("play")
        self.pause=self.builder.get_object("pause")
        self.stop=self.builder.get_object("stop")
        self.open=self.builder.get_object("open")

        #setting main window's size
        self.win.set_border_width(5)

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
    
