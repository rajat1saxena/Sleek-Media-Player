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

import gst,sys
import pygtk
pygtk.require("2.0")
import gtk,gobject
import gtk.glade
import playlist_reader
import re

class guibuild:
    #convert time - into readable form
    def convert_time(self, time=None):
        # convert_ns function from:
        # http://pygstdocs.berlios.de/pygst-tutorial/seeking.html
        # LGPL Version 3 - Copyright: Jens Persson
        if time==None:
            return None
        hours = 0
        minutes = 0
        seconds = 0
        time_string = ""
        time = time / 1000000000 # gst.NSECOND
        if time >= 3600:
            hours = time / 3600
            time = time - (hours * 3600)
        if time >= 60:
            minutes = time / 60
            time = time - (minutes * 60)
        #remaining time is seconds
        seconds = time
        time_string = time_string + str(hours).zfill(2) + ":" +str(minutes).zfill(2) + ":" + str(seconds).zfill(2)
        #return time in Hours:Minutes:Seconds format
        return time_string
    
    #hscale's value-changed callback function
    def callhscale(self,widget,event):
        print("hscale-tempered")
        value=widget.get_value()
        real_duration=self.mypipe.query_duration(self.time_format,None)[0]
        time=(value/self.adj.get_upper())*real_duration
        print("hscale value: "+str(value)+" time to be set: "+str(time))
        self.myplay.seek_simple(self.time_format,gst.SEEK_FLAG_FLUSH,time)
    
    #hscale callback function
    def update_hscale(self):
        if self.playflag==False:
            return False
        if self.playflag==True:
            self.length=self.mypipe.query_duration(self.time_format,None)[0]
            self.duration=self.convert_time(self.length)

            self.current_pos=self.mypipe.query_position(self.time_format,None)[0]
            self.current_position=self.convert_time(self.current_pos)
            
            
           #some logic for solving time format-for duration
            timelist1=self.duration.split(":")
            hours1=timelist1[0]
            minutes1=timelist1[1]
            seconds1=timelist1[2]
            totaltime1=(int(hours1)*3600+int(minutes1)*60+int(seconds1))
            #print(totaltime1)

            #some logic for solving time format-for current position
            timelist2=self.current_position.split(":")
            hours2=timelist2[0]
            minutes2=timelist2[1]
            seconds2=timelist2[2]
            totaltime2=(int(hours2)*3600+int(minutes2)*60+int(seconds2))
            #print(totaltime2)
            
            self.adj.set_upper(totaltime1)
            self.adj.set_value(totaltime2)
            #if totaltime1==totaltime2:
             #   self.on_stop(self.stop)
            #print(str(self.duration))
            return True
       
    #callback for BUS messages
    def on_message(self,bus,message):
        if message.type==gst.MESSAGE_EOS:
            print("end reached")
            if re.search(".pls$",self.originalfile):
                if self.playlist_pointer==len(self.tracklist)-1:
                    self.on_stop(self.stop)
                else:
                    self.on_next(self.next)
            else:
                self.on_stop(self.stop)
        elif message.type==gst.MESSAGE_ERROR:
            self.mypipe.set_state(gst.STATE_NULL)
            (err,debug)=message.parse_error()
            print("Error: %s"%err,debug)

    #A playlist_manager function to manage play of playlist
    def playlist_manager(self):
        #self.no_of_entries=len(self.tracklist)
        print("Successfull arrival at playlist_manager")
        self.mediafile=self.tracklist[self.playlist_pointer]
            
    # media control callbacks for play,pause and stop buttons      
    def on_play(self,widget):
        self.originalfile=self.open.get_filename()
        
        #Playlist logic
        if re.search(".pls$",self.originalfile):
            print("It's a playlist file")
            self.tracklist=playlist_reader.reader(self.originalfile).returner()
            print(self.tracklist)
            self.playlist_manager() #call to playlist_manager()
        else:
            self.mediafile="file://"+self.originalfile

        print(self.mediafile)
        self.win.set_title(self.mediafile)
        self.myplay.set_property("uri",self.mediafile)
        self.playflag=True
        self.timer=gobject.timeout_add(1000,self.update_hscale)
        self.mysink.set_xwindow_id(self.video.window.xid)
        self.mypipe.set_state(gst.STATE_PLAYING)
    def on_stop(self,widget):
        self.playflag=False
        self.adj.set_value(0)
        self.mypipe.set_state(gst.STATE_NULL)
    def on_pause(self,widget):
        self.playflag=False
        self.mypipe.set_state(gst.STATE_PAUSED)

    #Volume control call back
    def on_vol_change(self,widget,value=0.5):
        self.myplay.set_property("volume",float(value))
        return True
        
    #key press event detector
    def key_press(self,widget,event):
        #print("Key Code: "+str(event.keyval))
        if event.keyval==111:                #the key 'o'
            self.on_pause(self.pause)
        if event.keyval==112:                #the key 'p'
            self.on_play(self.play)
        if event.keyval==105:                 #the key 'i'
            self.on_stop(self.stop)
        if event.keyval==108:                 #the key 'l'
            self.on_next(self.next)
        if event.keyval==107:                 #the key 'k'
            self.on_prev(self.previous)
            
    #callbacks for previous and next buttons
    def on_prev(self,widget):
        if self.playlist_pointer==0:
            pass
        else:
            self.playlist_pointer=self.playlist_pointer-1
            self.on_stop(self.stop)
            self.on_play(self.play)

    def on_next(self,widget):
        if self.playlist_pointer==len(self.tracklist)-1:
            pass
        else:
            self.playlist_pointer=self.playlist_pointer+1
            self.on_stop(self.stop)
            self.on_play(self.play)


    # Initialiser function-Manages the gui,bus and gstreamer       
    def __init__(self):
        self.filename="./interface2.glade"
        self.builder=gtk.Builder()
        self.builder.add_from_file(self.filename)

        #initializing playlist pointer
        self.playlist_pointer=0

        #getting objects
        self.win=self.builder.get_object("mainwin")
        self.hbox=self.builder.get_object("hbox")
        self.play=self.builder.get_object("play")
        self.pause=self.builder.get_object("pause")
        self.stop=self.builder.get_object("stop")
        self.open=self.builder.get_object("open")
        self.previous=self.builder.get_object("previous")
        self.next=self.builder.get_object("next")
        self.video=self.builder.get_object("drawarea")
        self.volume=self.builder.get_object("appvolume")
        self.controltable=self.builder.get_object("sevotable")

        #creating hscale as it is not in glade file
        self.hscale=gtk.HScale()

        #setting drawing area's properties
        self.video.set_size_request(690,405)

        #setting volume button's property
        self.volume.connect("value-changed",self.on_vol_change)

        #attching seekbar to sevotable
        self.controltable.attach(self.hscale,0,1,0,3)

        #setting main window's size
        self.win.set_border_width(5)
        self.win.set_size_request(700,500)

        #setting hscale properties
        self.hscale.connect("button-release-event",self.callhscale)
        self.duration=None
        self.adj=gtk.Adjustment()
        self.adj.set_lower(0)
        self.adj.set_page_increment(1.0)
        self.hscale.set_adjustment(self.adj)
        self.hscale.set_update_policy(gtk.UPDATE_DISCONTINUOUS)

        #setting drawing area's size
        #self.video.set_size_request(800,650)

        #connecting objects with callback functions
        self.win.connect("destroy",gtk.main_quit)
        self.win.connect("key-press-event",self.key_press)
        self.play.connect("clicked",self.on_play)
        self.pause.connect("clicked",self.on_pause)
        self.stop.connect("clicked",self.on_stop)
        self.previous.connect("clicked",self.on_prev)
        self.next.connect("clicked",self.on_next)

        #setting filechooser button's properties
        self.open.set_current_folder("/home")

        #creating gst playbin to play media file
        self.myplay=gst.element_factory_make("playbin2","Player")
        self.mysink=gst.element_factory_make("xvimagesink","Sink")
        self.mypipe=gst.Pipeline("mypipeline")
        self.mysink.set_property('force-aspect-ratio',True)
        self.myplay.set_property('video-sink',self.mysink)
        self.mypipe.add(self.myplay)
        self.bus=self.mypipe.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message",self.on_message)
        
        #settings related to timer        
        self.playflag=False                                        #this will be used to represent state of player
        self.time_format=gst.Format(gst.FORMAT_TIME)


        #showing the main window
        self.win.show_all()
    
if __name__=="__main__":
    mybuild=guibuild()
    gtk.main()
    
