using System;
using System.IO;
using System.Windows.Forms;
using ScintillaNET;
using System.Drawing;
using System.Text;
using System.Threading;
using System.Windows.Forms.VisualStyles;
using System.Diagnostics;
using System.ComponentModel;

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
        private ThreadStart delegado, del;
        private Thread hilo, hilo2;
        private String filepath = "";
        private BackgroundWorker worker;
        private const string PYTHON = @"C:\Python27\pythonw.exe";
        public Form1()
        {
            InitializeComponent();
            worker = new BackgroundWorker();
            worker.WorkerReportsProgress = true;
            worker.WorkerSupportsCancellation = true;

            worker.DoWork += new DoWorkEventHandler(worker_DoWork);
            worker.ProgressChanged += new ProgressChangedEventHandler(worker_ProgressChanged);
            worker.RunWorkerCompleted += new RunWorkerCompletedEventHandler(worker_RunWorkerCompleted);



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

            TextArea.StyleResetDefault();
            TextArea.Styles[Style.Default].Font = "Consolas";
            TextArea.Styles[Style.Default].Size = 15;
            TextArea.StyleClearAll();
            
            TextArea.Styles[Style.Cpp.Identifier].ForeColor = Color.DeepPink;
            TextArea.Styles[Style.Cpp.Number].ForeColor = Color.Red;
            TextArea.Styles[Style.Cpp.Word].ForeColor = Color.Navy;
            TextArea.Styles[Style.Cpp.CommentLine].ForeColor =Color.Gray;
            TextArea.Styles[Style.Cpp.Comment].ForeColor = Color.ForestGreen;
            TextArea.Lexer = Lexer.Cpp;
            TextArea.SetKeywords(0, "main if then else end do while repeat until cin cout real int boolean");


            delegado = new ThreadStart(FilasYColumnas);

            hilo = new Thread(delegado);

            hilo.Start();

            
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
        private void construir()
        {

            string comando = "python  automata.py " + FileName;
            string error, final;
            string[] error1, final1;
            try
            {
                error = FileName.Replace("mcp", "err");
                final = FileName.Replace("mcp", "fin");
            }catch(Exception e)
            {

            }
            // comando = "echo('Hola')";

            //   Process cmd = new Process();
            ProcessStartInfo cmd = new ProcessStartInfo();

            //  cmd.StartInfo.FileName = "cmd.exe";
            cmd.FileName = @"C:\Python27\pythonw.exe";
            cmd.Arguments = " automata.py " + FileName;
            Process proc = new Process();
            proc.StartInfo=cmd;
            proc.Start();
            proc.WaitForExit(); 
            











           // cmd.StartInfo.RedirectStandardInput = true;
           // cmd.StartInfo.RedirectStandardOutput = true;
            //cmd.StartInfo.CreateNoWindow = true;
            //cmd.StartInfo.UseShellExecute = false;
            //cmd.Start();


          //  cmd.StandardInput.WriteLine(comando);
           // cmd.StandardInput.Flush();
           // cmd.StandardInput.Close();
           // cmd.WaitForExit();
            
            //lexicoText.Text = cmd.StandardOutput.ReadToEnd();
            //lexicErr.Text = FileName;

            // lexicoText.Text = final;

            //error1= System.IO.File.ReadAllLines(error); 
            //final1 = System.IO.File.ReadAllLines(final);
           /* System.IO.StreamReader err = new System.IO.StreamReader(error);
            System.IO.StreamReader fin = new System.IO.StreamReader(final);

            string linea1, linea2;

            while ((linea1 = err.ReadLine()) != null)
           {
             lexicErr.AppendText(linea1);
            }

            while ((linea2 = fin.ReadLine()) != null)
            {
                lexicoText.AppendText(linea2);
            }*/
            /*this.Invoke((MethodInvoker)delegate
            {
                // lexicErr.Text = System.IO.File.ReadAllText(error);
                for(int i=0; i<final1.Length;i++)
                lexicoText.Text += final1[i];
            });
            this.Invoke((MethodInvoker)delegate
            {
                for (int i = 0; i < final1.Length; i++)
                    lexicErr.Text = error1[i];
                // lexicoText.Text = System.IO.File.ReadAllText(final);
            });*/

        }
        void worker_DoWork(object sender, DoWorkEventArgs e)
        {
            construir();
        }
        void worker_RunWorkerCompleted(object s, RunWorkerCompletedEventArgs e)
        {
            string error, final;

            error = FileName.Replace("mcp", "err");
            final = FileName.Replace("mcp", "fin");
            // System.IO.StreamReader err = new System.IO.StreamReader(error);
            //System.IO.StreamReader fin = new System.IO.StreamReader(final);

            //string linea1, linea2;

            //while ((linea1 = err.ReadLine()) != null)
            //{
            //  lexicErr.AppendText(linea1);
            //}

            //while ((linea2 = fin.ReadLine()) != null)
            //{
            //  lexicoText.AppendText(linea2);
            //}


            //this.Invoke((MethodInvoker)delegate
            //{
                try
                {
                    lexicErr.Text = System.IO.File.ReadAllText(error);
                }catch(Exception ex)
                {
                    //Console.Write(e.ToString);
                }

           // });
           // this.Invoke((MethodInvoker)delegate
            //{
                lexicoText.Text = System.IO.File.ReadAllText(final);
            //});
            toolStripButton1.Enabled = true;
            buildToolStripMenuItem.Enabled = true;

        }

        private void buildToolStripMenuItem_Click(object sender, EventArgs e)
        {
            lexico();
        }

        void worker_ProgressChanged(object s, ProgressChangedEventArgs e)
        {
            
        }

        private void toolStripButton1_Click(object sender, EventArgs e)
        {
            lexico();
           
        }
        private void lexico()
        {
            if (TextArea.Text == "" || TextArea.Text == null  )
            {
                MessageBox.Show("No se puede aplicar el Script Lexico si no hay datos ", "WARNING", MessageBoxButtons.OK);
            }
            else
            {
                //construir();
                eleccionGuardar();
                worker.RunWorkerAsync();
                toolStripButton1.Enabled = false;
                buildToolStripMenuItem.Enabled = false;
            }
        }
    }
}
