import gi
from pytube import YouTube

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gio

class CoreWindow(Gtk.Window):
    def __init__(self):
        #Edición de la ventana principal
        super().__init__(title="PyTube Downloader")
        self.set_border_width(50)
        self.set_size_request(800, 600)
        self.set_resizable(False)
        
        self.header_bar=Gtk.HeaderBar()
        self.header_bar.set_show_close_button(True)
        self.header_bar.props.title = "PyTube Downloader"
        self.set_titlebar(self.header_bar)
        
      
        self.btn_selectFile = Gtk.FileChooserButton(title="Seleccione carpteta de destino")
        self.btn_selectFile.set_current_folder("/home")
        self.btn_selectFile.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        
        self.lbl_selectFile = Gtk.Label()
        self.lbl_selectFile.set_text("Escoja la ruta de destino")
        
        self.ent_entry = Gtk.Entry()
        self.ent_entry.set_placeholder_text("Ingrese el URL de video de YouTube")
        
        calidad=["La mayor calidad de video posible",
                 "La menor calidad de video posible",
                 "Solo audio"]
        self.btn_aceptar = Gtk.Button()
        self.btn_aceptar.set_label("ACEPTAR")
        self.btn_aceptar.connect("clicked", self.aceptar)
        
        
        self.lbl_info= Gtk.Label()
        self.lbl_info.set_text("INFO:\n" "Titulo:\n" "Duracion:\n" "Visitas:")
        self.lbl_entry=Gtk.Label()
        self.lbl_entry.set_text("Ingrese el URL de video de YouTube")
        
        
        self.calidad_combo = Gtk.ComboBoxText()
        self.calidad_combo.set_entry_text_column(0)
        for calidades in calidad:
            self.calidad_combo.append_text(calidades)
        self.lbl_combo= Gtk.Label()
        self.lbl_combo.set_text("Escoja la calidad de su video")
        
        self.btn_descargar=Gtk.Button(label="DESCARGAR")
        self.btn_descargar.connect("clicked",self.descargar)
        
        
        self.list_store=Gtk.ListStore(str,int,bool)

        self.renderer_text = Gtk.CellRendererText()
        self.column_text = Gtk.TreeViewColumn("Text", self.renderer_text, text=0)

        self.renderer_progress = Gtk.CellRendererProgress()
        self.column_progress = Gtk.TreeViewColumn(
            "Progress", self.renderer_progress, value=1, inverted=2
        )
        """treeview.append_column(column_progress)
        self.on_inverted_toggled=False
        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_inverted_toggled)
        column_toggle = Gtk.TreeViewColumn("Inverted", renderer_toggle, active=2)
        treeview.append_column(column_toggle)"""
        
        
        grid = Gtk.Grid()
        grid.attach(self.header_bar,0,0,1,1)
        grid.set_column_spacing(110)
        grid.set_row_spacing(30)
        grid.attach(self.lbl_entry,0,0,4,1)
        grid.attach(self.ent_entry, 0, 1, 4, 1)
        grid.attach(self.lbl_info, 0,2,3,1)
        grid.attach(self.btn_descargar,2,5,2,1)
        grid.attach_next_to(self.btn_aceptar,self.ent_entry,Gtk.PositionType.RIGHT,1,1)
        grid.attach_next_to(self.lbl_combo,self.lbl_info,Gtk.PositionType.BOTTOM, 3, 1)
        grid.attach_next_to(self.calidad_combo,self.lbl_combo,Gtk.PositionType.BOTTOM,3,1)
        grid.attach_next_to(self.lbl_selectFile,self.lbl_combo,Gtk.PositionType.RIGHT,3,1)
        grid.attach_next_to(self.btn_selectFile,self.lbl_selectFile,Gtk.PositionType.BOTTOM,3,1)
        
        """grid.attach_next_to(self.list_store,self.calidad_combo,Gtk.PositionType.BOTTOM, 2, 4)"""
        self.add(grid)
        
    def aceptar(self,widget):
        self.link=self.ent_entry.get_text()
        self.video= YouTube(self.link)
        titulo= self.video.title
        duracion= round(self.video.length/60,2)
        visitas= self.video.views
        print(titulo,duracion,visitas)
        self.lbl_info.set_text("INFO: \n" "Titulo: %s\n" "Duracion: %d minutos\n" "Visitas: %d"
                               %(titulo,duracion,visitas))
    
    def descargar(self,widget):
        self.des_calidad=self.calidad_combo.get_active_text()
        self.des_selectFile=self.btn_selectFile.get_filename()
        print(self.des_calidad,self.des_selectFile)
        if self.des_calidad=="La mayor calidad de video posible":
            self.video.streams.get_highest_resolution().download(self.des_selectFile)
            print("listo")
        elif self.des_calidad=="La menor calidad de video posible":
            self.video.streams.get_worst_resolution().download(self.des_selectFile)
            print("listo")
        elif self.des_calidad=="Solo audio":
            self.video.streams.get_audio_only().download(self.des_selectFile)
            print("listo")
        else:
            print("no hay nada")
            
        
        
        
win = CoreWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()