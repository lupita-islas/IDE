using System;
using System.IO;
using System.Windows.Forms;
using ScintillaNET;
using System.Drawing;
using System.Text;
using System.Threading;
using System.Windows.Forms.VisualStyles;

namespace Compi
{
    public partial class Form1 : Form
    {
        ScintillaNET.Scintilla TextArea;
        private const int NUMBER_MARGIN = 1;
        private const int BACK_COLOR = 0x2A211C;
        private const int FORE_COLOR = 0xB7B7B7;
        private bool guardPrimeraVez;
        private String FileName;
        private ThreadStart delegado;
        private Thread hilo;
        private String filepath = "";
        public Form1()
        {
            InitializeComponent();
        }

        private void archivoToolStripMenuItem_Click(object sender, EventArgs e)
        {

        }

        private void toolStrip1_ItemClicked(object sender, ToolStripItemClickedEventArgs e)
        {

        }

        private void Form1_Load(object sender, EventArgs e)
        {
            TextArea = new ScintillaNET.Scintilla();
            TextPanel.Controls.Add(TextArea);
            TextArea.Dock = System.Windows.Forms.DockStyle.Fill;
            TextArea.TextChanged += (this.OnTextChanged);
            TextArea.WrapMode = WrapMode.Word;
            InitNumberMargin();

            delegado = new ThreadStart(FilasYColumnas);

            hilo = new Thread(delegado);

            hilo.Start();

            //FilasYColumnas();
        }

        private void InitNumberMargin()
        {
            TextArea.Styles[Style.LineNumber].BackColor = IntToColor(BACK_COLOR);
            TextArea.Styles[Style.LineNumber].ForeColor = IntToColor(FORE_COLOR);
            var nums = TextArea.Margins[NUMBER_MARGIN];
            nums.Width = 30;
            nums.Type = MarginType.Number;
            nums.Mask = 0;
        }
        public static Color IntToColor(int rgb)
        {
            return Color.FromArgb(255, (byte)(rgb >> 16), (byte)(rgb >> 8), (byte)rgb);
        }
        private void OnTextChanged(object sender, EventArgs e)
        {
           
        }

        private void panel2_Paint(object sender, PaintEventArgs e)
        {

        }

        private void guardarSimple()
        {
            using (StreamWriter writer = new StreamWriter(FileName, false, Encoding.UTF8))
            {
                writer.Write(TextArea.Text);
            }
            guardPrimeraVez = true;
        }
        private void abrirArchivo()
        {
            guardPrimeraVez = true;
            Stream stream = null;
            String FILTRO = "Archivos Mi Compilador |*.mcp";
            String TITULO = "Selecciona un Archivo .mcp";
            String ERR = "Error al abrir el archivo";
            OpenFileDialog abrir = new OpenFileDialog();
            abrir.Filter = FILTRO;
            abrir.Title = TITULO;
            
            if (abrir.ShowDialog() == DialogResult.OK)
            {
                FileName = abrir.FileName;
                try
                {
                    if ((stream = abrir.OpenFile()) != null)
                    {
                        using (StreamReader sr = new StreamReader(stream))
                        {
                            String line = sr.ReadToEnd();
                            if (TextArea.Text == "")
                            {
                                this.Text += "   "+FileName;
                                TextArea.Text = line;
                            }
                            else
                            {
                                DialogResult res = MessageBox.Show("Desea abrir otro archivo sin guar" +
                                                                   "dar el que esta abierto?","Important Question", MessageBoxButtons.YesNo );
                                if (res == DialogResult.Yes)
                                {
                                    TextArea.Text = line;
                                }
                                
                            }
                           
                            
                        }
                    }
                }
                catch (Exception ex)
                {
                    MessageBox.Show(ERR);
                }
            }

        }
          
        private void guardarArchivoNuevo()
        {

            String FILTRO = "Mi Compilador |*.mcp";
            String TITULO = "Guardar un archivo Mi Compilador";

            SaveFileDialog guardar = new SaveFileDialog();
            guardar.Filter = FILTRO;
            guardar.Title = TITULO;
            
            
            if (guardar.ShowDialog()== DialogResult.OK)
            {
                FileName = guardar.FileName;
                File.WriteAllText(guardar.FileName, TextArea.Text); //aqui poner el text area
            }
            this.Text = "Monkey IDE   "+FileName;
            guardPrimeraVez = true;
        }

        private void openToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            abrirArchivo();

        }

        private void abrir_Click(object sender, EventArgs e)
        {
            abrirArchivo();
        }

        private void saveToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            eleccionGuardar();
        }

        private void saveAsToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            guardarArchivoNuevo();
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {

            
            DialogResult res= MessageBox.Show("Desea guardar los cambios", "Important Question", MessageBoxButtons.YesNo);
            if (res == DialogResult.Yes)
            {
                eleccionGuardar();
            }
            ///aqui se debe detener el hilo
            hilo.Abort();
        }

        private void guardar_Click(object sender, EventArgs e)
        {
            eleccionGuardar();
        }

        private void eleccionGuardar()
        {
            if (!guardPrimeraVez)
            {
                guardarArchivoNuevo();
            }
            else
            {
                guardarSimple();
            }
        }

        private void newToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            nuevoArchivo();
        }

        private void nuevoArchivo()
        {
           
            if (TextArea.Text != "")
            {

                DialogResult res = MessageBox.Show("Desea guardar los cambios? ","Important Question",MessageBoxButtons.YesNo);
                if (res == DialogResult.Yes)
                {
                    eleccionGuardar();
                    TextArea.Text = "";
                    guardPrimeraVez = false;
                }
            }
            else
            {
                TextArea.Text = "";
                
            }
       }

        private void nuevo_Click(object sender, EventArgs e)
        {
            nuevoArchivo();
        }

        private void semantico_Click(object sender, EventArgs e)
        {

        }

       
        private void FilasYColumnas()
        {
            while (true)
            {
                try
                {
                    this.Invoke((MethodInvoker) delegate
                    {

                        var cu = TextArea.CurrentPosition;
                        var f = TextArea.CurrentLine;
                        var co = TextArea.GetColumn(cu);

                        filas.Text = " " + (f + 1);
                        columnas.Text = " " + (co + 1 );

                    });
                }
                catch (Exception ex)
                {
                    
                }
            }






        }
    }
}
