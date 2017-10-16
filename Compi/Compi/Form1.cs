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
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using System.Data;

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
        private const string PYTHON = @"C:\Python27\python.exe";
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
            nums.Width = 60;
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
                }else
                {
                    TextArea.Text = "";
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
            string error, final,errorSintac,volcado="";
            //string[] error1, final1;
            try
            {
                volcado = FileName.Replace("mcp", "vol");
                errorSintac = FileName.Replace("mcp", "errS");
                error = FileName.Replace("mcp", "err");
                final = FileName.Replace("mcp", "fin");
                
            } catch (Exception e)
            {

            }
           
            ProcessStartInfo cmd = new ProcessStartInfo();
            ProcessStartInfo cmd2 = new ProcessStartInfo();
            ProcessStartInfo cmd3 = new ProcessStartInfo();
            //  cmd.StartInfo.FileName = "cmd.exe";
            cmd.FileName = @"C:\Program Files (x86)\Python36-32\python.exe";
            cmd2.FileName= @"C:\Program Files (x86)\Python36-32\python.exe";
            cmd3.FileName = @"C:\Program Files (x86)\Python36-32\python.exe";
            cmd.Arguments = " automata.py " + FileName;
            cmd2.Arguments = "gramatica.py " + volcado;
            cmd3.Arguments = "semantico.py " + volcado; 
            cmd.RedirectStandardOutput = false;
            cmd2.RedirectStandardOutput = false;
            cmd3.RedirectStandardOutput = false;
            cmd.UseShellExecute = false;
            cmd2.UseShellExecute = false;
            cmd3.UseShellExecute = false;
            cmd.CreateNoWindow = true;
            cmd2.CreateNoWindow = true;
            cmd3.CreateNoWindow = true;
            Process proc = new Process();
            Process proc2 = new Process();
            Process proc3 = new Process();
            proc.StartInfo = cmd;
            proc2.StartInfo = cmd2;
            proc3.StartInfo = cmd3;
            try
            {
                proc.Start();
                //  var ou = proc.StandardOutput.ReadToEnd();
                /*while(!proc.HasExited && proc.Responding)
                {
                    Thread.Sleep(10);
                }*/
                proc.WaitForExit();
                Console.WriteLine("Proceso1");
                //Thread.Sleep(5000);
                if (proc.HasExited)
                {
                    proc2.Start();
                    proc2.WaitForExit();
                    Console.WriteLine("Proceso2");
                    if (proc2.HasExited)
                    {
                        proc3.Start();
                        proc3.WaitForExit();
                        Console.WriteLine("Proceso3");
                    }
                }
            }
            catch(Exception a)
            {
                Console.WriteLine("Error XDDD");
                a.ToString();
            }
           


        }
        void worker_DoWork(object sender, DoWorkEventArgs e)
        {
            construir();
        }
        void worker_RunWorkerCompleted(object s, RunWorkerCompletedEventArgs e)
        {
            string error, final,errorSintac,arbolText,regx,tabla,errSem,arbolSem,regx2;

            error = FileName.Replace("mcp", "err");
            final = FileName.Replace("mcp", "fin");
            errorSintac = FileName.Replace("mcp", "errS");
            arbolText = FileName.Replace("mcp", "tree");
            tabla = FileName.Replace("mcp", "table");
            errSem = FileName.Replace("mcp", "errSem");
            arbolSem = FileName.Replace("mcp", "treeSint");
            List<string> listaNodos = new List<string>();
            List<string> listaNodosSem = new List<string>();
            regx = @"(?:\d*\.)?\d+";
            

            Regex rgx = new Regex(regx);
           
            try{ 
                
                lexicErr.Text = System.IO.File.ReadAllText(error);
                errSint.Text = System.IO.File.ReadAllText(errorSintac);
                lexicoText.Text = System.IO.File.ReadAllText(final);
                string[] lineas = System.IO.File.ReadAllLines(arbolText);
                string[] lineasSem = System.IO.File.ReadAllLines(arbolSem);
                string[] tablaInfo = System.IO.File.ReadAllLines(tabla);
                errSemtx.Text = System.IO.File.ReadAllText(errSem);
                for (int i=0; i<lineas.Length;i++){
                    
                    /* var arrStr = lineas[i].Split('|');
                                      
                        Double.TryParse(arrStr[arrStr.Length - 1], out var n);
                      lineas[i] = rgx.Replace(lineas[i], "");
                                        
                        if (n != 0)
                        {
                            lineas[i] += arrStr[arrStr.Length - 1];
                        }
                        */
                        listaNodos.Add(lineas[i]);
                       
                }
                for(int i = 0; i < lineasSem.Length; i++)
                {
                    
                    var splitedLine = lineasSem[i].Split(',');
                   /* for(int j = 1; j < splitedLine.Length; j++)
                    {
                        if (splitedLine[j].Contains("type") || splitedLine[j].Contains("value"))
                        {
                            
                          
                            splitedLine[0] += " " + splitedLine[j];
                        }
                    }
                    */
                    
                    
                   // splitedLine[0] = rgx2.Replace(splitedLine[0], " ");
                    Console.WriteLine(splitedLine[0]);
                    listaNodosSem.Add(splitedLine[0]);
                }



                //treeView.Nodes.Add(PopulateTreeNode2(listaNodos, "/"));

                //LoadTreeViewFromFile(arbolText, treeView);
                PopulateTreeView(treeView, listaNodos, '|');
                PopulateTreeView(treeViewSem, listaNodosSem, '|');
                PopulateTreeView(treeView2, listaNodosSem, '|');
                treeView.ExpandAll();
                treeViewSem.ExpandAll();
                treeView2.ExpandAll();
                

                dataGrid.DataSource = llenarTabla(tablaInfo);
                
                

                //arbol.Text = System.IO.File.ReadAllText(arbolText);
            }
            catch(Exception ex)
                {
                    Console.WriteLine("Error de archivos");
                    Console.WriteLine(ex.ToString());
                }
            
           
            toolStripButton1.Enabled = true;
            buildToolStripMenuItem.Enabled = true;

        }
        private DataTable llenarTabla(string[] tablaInfo)
        {
            
            DataTable table = new DataTable();
            table.Columns.Add("Nombre", typeof(string));
            table.Columns.Add("Tipo", typeof(string));
            table.Columns.Add("Memoria", typeof(string));
            table.Columns.Add("Valor", typeof(string));
            table.Columns.Add("Lineas", typeof(string));
            for (int i = 0; i < tablaInfo.Length; i++)
            {
                var camposArr = tablaInfo[i].Split('|');
                table.Rows.Add(camposArr[0], camposArr[1], camposArr[2], camposArr[3], camposArr[4]);

            }
            return table;
           
        }
        private void buildToolStripMenuItem_Click(object sender, EventArgs e)
        {
            lexico();
        }

        void worker_ProgressChanged(object s, ProgressChangedEventArgs e)
        {
            
        }

        private void TextPanel_Paint(object sender, PaintEventArgs e)
        {

        }

        private void aboutToolStripMenuItem_Click(object sender, EventArgs e)
        {
            MessageBox.Show("IDE Hecho por: \n Ruth Guadalupe Islas Ortega \n César Omar Rodríguez Huerta \n Todos Los Derechos Reservados 2017\n UAA","INFO",MessageBoxButtons.OK);
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

        //private TreeNode PopulateTreeNode2(string[] paths, string pathSeparator)
        private TreeNode PopulateTreeNode2(List<string> paths, string pathSeparator)
        {
            if (paths == null)
                return null;

            TreeNode thisnode = new TreeNode();
            TreeNode currentnode;
            char[] cachedpathseparator = pathSeparator.ToCharArray();
            foreach (string path in paths)
            {
                currentnode = thisnode;
                foreach (string subPath in path.Split(cachedpathseparator))
                {
                    if (null == currentnode.Nodes[subPath])
                        currentnode = currentnode.Nodes.Add(subPath, subPath);
                    else
                        currentnode = currentnode.Nodes[subPath];
                }
            }

            return thisnode;
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }

        private void tableLayoutPanel1_Paint(object sender, PaintEventArgs e)
        {

        }

        private static void PopulateTreeView(TreeView treeView, List<string> paths, char pathSeparator)
        {
            TreeNode lastNode = null;
            string subPathAgg;
            foreach (string path in paths)
            {
                subPathAgg = string.Empty;
                foreach (string subPath in path.Split(pathSeparator))
                {
                    subPathAgg += subPath + pathSeparator;
                    TreeNode[] nodes = treeView.Nodes.Find(subPathAgg, true);
                    if (nodes.Length == 0)
                        if (lastNode == null)
                            lastNode = treeView.Nodes.Add(subPathAgg, subPath);
                        else
                            lastNode = lastNode.Nodes.Add(subPathAgg, subPath);
                    else
                        lastNode = nodes[0];
                }
                lastNode = null; // This is the place code was changed

            }
        }

        // Load a TreeView control from a file that uses tabs
        // to show indentation.
        private void LoadTreeViewFromFile(string file_name, TreeView trv)
        {
            // Get the file's contents.
            string file_contents = File.ReadAllText(file_name);

            // Break the file into lines.
            string[] lines = System.IO.File.ReadAllLines(file_name);
            /*string[] lines = file_contents.Split(
                new char[] { '\r', '\n' },
                StringSplitOptions.RemoveEmptyEntries);*/

            // Process the lines.
            trv.Nodes.Clear();
            Dictionary<int, TreeNode> parents = new Dictionary<int, TreeNode>();
            foreach (string text_line in lines)
            {
                // See how many tabs are at the start of the line.
                int level = text_line.Length -text_line.TrimStart('\t').Length;
                Console.WriteLine(text_line.TrimStart('\t').Length);

                // Add the new node.
                if (level == 0)
                    parents[level] = trv.Nodes.Add(text_line.Trim());
                else
                    parents[level] =parents[level - 1].Nodes.Add(text_line.Trim());
                parents[level].EnsureVisible();
            }

            if (trv.Nodes.Count > 0) trv.Nodes[0].EnsureVisible();
        }
        private static void PopulateTreeViewSem(TreeView treeView, List<string> paths, char pathSeparator)
        {
            TreeNode lastNode = null;
            string subPathAgg="",subPathAggBus="";
            foreach (string path in paths)
            {
                subPathAgg = string.Empty;
                foreach (string subPath in path.Split(pathSeparator))
                {
                    var temporal = subPath.Split(null);

                    
                    subPathAggBus = subPathAgg+temporal[0] + pathSeparator;
                    subPathAgg += subPath + pathSeparator;

                    TreeNode[] nodes = treeView.Nodes.Find(subPathAggBus, true);
                    if (nodes.Length == 0)
                        if (lastNode == null)
                            lastNode = treeView.Nodes.Add(subPathAgg, subPath);
                        else
                            lastNode = lastNode.Nodes.Add(subPathAgg, subPath);
                    else
                        lastNode = nodes[0];
                }
                lastNode = null; // This is the place code was changed

            }
        }

    }

}
