# Hades Logic Design Assignment Completion Program
Hades, the King of the Underworld will fulfill your one last wish of completing your Logic Design Assignment.

Directory structure:

- hades-logic-design-assignment-master
  - hades.py
  - stuffs
      - library.v
      - scaffolds
          - 01m.v
          - 01s.v
          - 02m.v
          - 02s.v
      - crafts
          - your_completed_assignment_folder
      - furnace
          - test_files

Create folders: Create a new folder stuff containing folders scaffolds, crafts, furnace.

Put all code under the folder scaffolds.

File containing module must be module must be named ##m.v where ## is the question number in 2 digit representation. eg: 01m.v, 12m.v

File containing module must be simulation must be named ##s.v where ## is the question number in 2 digit representation. eg: 01s.v, 24s.v

Put the definitions for different modules under the file library.v in folder stuff.

Your library file looks like this:
```verilog
@module-1-name
module module_1_name(a,b)
//something
endmodule
```

Your module file will look like:
```verilog
@module-1-name
@module-2-name
@main-module-name
```

Your simulate file will look like:
```verilog
module simulate;
//something
endmodule
```

Open terminal/cmd and call hades:
```bash
python3 hades.py
```

Hades will replace the catchphrase-slots (`@module-name`) in module files from the folder scaffolds with their definitions/patches in library.v from the folder stuffs.

He will compile and run the simulation for you and show the errors or outputs if any.
