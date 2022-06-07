import gi
from pytube import YouTube
from about import About
import time

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gio

class CoreWindow(Gtk.Window):
    def __init__(self):
        #Edición de la ventana principal
        super().__init__(title="PyTube Downloader")
        self.set_border_width(50)
        self.set_size_request(920,920)
        self.set_resizable(False)
        
        
        btn_about = Gtk.Button()
        btn_about.set_label("❓")
        btn_about.connect("clicked", self.aboutShow)
        
        
        self.header_bar=Gtk.HeaderBar()
        self.header_bar.set_show_close_button(True)
        self.header_bar.props.title = "PyTube Downloader"
        self.header_bar.pack_end(btn_about)

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

        self.liststore = Gtk.ListStore(str,str,str,int)
        treeview = Gtk.TreeView(model=self.liststore)
        render_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Nombre", render_text, text=0)
        treeview.append_column(column_text)
        
        render_text1 = Gtk.CellRendererText()
        column_text1 = Gtk.TreeViewColumn("Ubicacion", render_text1, text=0)
        treeview.append_column(column_text1)
        
        render_text2 = Gtk.CellRendererText()
        column_text2 = Gtk.TreeViewColumn("Estado", render_text2, text=0)
        treeview.append_column(column_text2)
        
        render_progress = Gtk.CellRendererProgress()
        column_progress = Gtk.TreeViewColumn("Progreso",render_progress)
        treeview.append_column(column_progress)
        
        
        
        
        
        
        
        
        rll_red = Gtk.ScrolledWindow()
        rll_red.set_vexpand(True)
        rll_red.set_hexpand(True)

        rll_red.add(treeview)
        
        
        
        
        
        
        
        grid = Gtk.Grid()
        grid.set_column_spacing(110)
        grid.set_row_spacing(30)
        grid.attach(self.lbl_entry,0,0,5,1)
        grid.attach(self.ent_entry, 0, 1, 5, 1)
        grid.attach(self.lbl_info, 0,2,3,1)
        grid.attach(self.btn_descargar,2,6,3,1)
        grid.attach_next_to(self.btn_aceptar,self.ent_entry,Gtk.PositionType.RIGHT,2,1)
        grid.attach_next_to(self.lbl_combo,self.lbl_info,Gtk.PositionType.BOTTOM, 3, 1)
        grid.attach_next_to(self.calidad_combo,self.lbl_combo,Gtk.PositionType.BOTTOM,3,1)
        grid.attach_next_to(self.lbl_selectFile,self.lbl_combo,Gtk.PositionType.RIGHT,4,1)
        grid.attach_next_to(self.btn_selectFile,self.lbl_selectFile,Gtk.PositionType.BOTTOM,4,1)
        
        
        infoBox = Gtk.Box(orientation = 1, spacing = 0)

        infoBox.pack_start(grid, False, True, 0)
        
        mainBox = Gtk.VBox(spacing = 20)

        mainBox.pack_end(rll_red, False, True, 0)
        mainBox.pack_start(infoBox, False, True, 0)

        
    
        """grid.attach_next_to(self.list_store,self.calidad_combo,Gtk.PositionType.BOTTOM, 2, 4)"""
        self.add(mainBox)
        
    def aceptar(self,widget):
        self.link=self.ent_entry.get_text()
        self.video= YouTube(self.link)
        self.titulo= self.video.title
        duracion= round(self.video.length/60,2)
        visitas= self.video.views
        print(self.titulo,duracion,visitas)
        self.lbl_info.set_text("INFO: \n" "Titulo: %s\n" "Duracion: %d minutos\n" "Visitas: %d"
                               %(self.titulo,duracion,visitas))
    


    def empezar(self):
        print(self.des_calidad,self.des_selectFile)
        if self.des_calidad=="La mayor calidad de video posible":
            self.video.streams.get_highest_resolution().download(self.des_selectFile)
            print("listo")
        elif self.des_calidad=="La menor calidad de video posible":
            self.video.streams.get_lowest_resolution().download(self.des_selectFile)
            print("listo")
        elif self.des_calidad=="Solo audio":
            self.video.streams.get_audio_only().download(self.des_selectFile)
            print("listo")
        else:
            print("no hay nada")
            
    def descargar(self,widget):
        self.des_selectFile=self.btn_selectFile.get_filename()
        self.liststore.append([self.titulo,self.des_selectFile,"Descargando", 0])
        self.des_calidad=self.calidad_combo.get_active_text()
        self.empezar()
            
    def aboutShow(self, widget):
        About(self)
    
            
        
        
        
win = CoreWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()