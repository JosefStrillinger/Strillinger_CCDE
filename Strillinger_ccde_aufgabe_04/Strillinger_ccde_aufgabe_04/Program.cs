using System;
using System.Collections.Generic;
using System.IO;

namespace Strillinger_ccde_aufgabe_04 {
    class Program {

        static void Main(string[] args) {
            string fileName = @"D://HTL-Anichstraße/Cloud_Computing/4a.txt";
            string fileName2 = @"D://HTL-Anichstraße/Cloud_Computing/4b.txt";

            string commands = generateAddUser(fileName);
            Console.WriteLine(commands);
            string commands2 = generateAddUser(fileName2);
            Console.WriteLine(commands2);

            string commandsAdd = generateAddToGroup(fileName);
            Console.WriteLine(commandsAdd);
            string commandsAdd2 = generateAddToGroup(fileName2);
            Console.WriteLine(commandsAdd2);

            string commandsDel = generateDelUser(fileName);
            Console.WriteLine(commandsDel);
            string commandsDel2 = generateDelUser(fileName2);
            Console.WriteLine(commandsDel2);

        }

        public static string generateAddUser(string path) {
            string command = "";
            string lines = File.ReadAllText(path);
            lines = lines.Replace("\t", " ");
            lines = lines.Replace(" ", "_");
            string[] names = lines.Split("\n", StringSplitOptions.None);
            foreach (string name in names) {
                string addUserCommand = "sudo useradd ";
                command += addUserCommand + name+"\n";
                

            }
            return command;
        }

        public static string generateDelUser(string path) {
            string command = "";
            string lines = File.ReadAllText(path);
            lines = lines.Replace("\t", " ");
            lines = lines.Replace(" ", "_");
            string[] names = lines.Split("\n", StringSplitOptions.None);
            foreach (string name in names) {
                string addUserCommand = "sudo userdel ";
                command += addUserCommand + name + "\n";


            }
            return command;
        }

        public static string generateAddToGroup(string path) {
            string group = "";
            if (path.Equals(@"D://HTL-Anichstraße/Cloud_Computing/4a.txt")) {
                group = "htlinn_4a";
            } else if (path.Equals(@"D://HTL-Anichstraße/Cloud_Computing/4b.txt")) {
                group = "htlinn_4b";
            }
            string command = "";
            string lines = File.ReadAllText(path);
            lines = lines.Replace("\t", " ");
            lines = lines.Replace(" ", "_");
            string[] names = lines.Split("\n", StringSplitOptions.None);
            foreach (string name in names) {
                string addUserCommand = "sudo usermod -G "+group+" ";
                command += addUserCommand + name + "\n";


            }
            return command;
        }

    }

    
}
