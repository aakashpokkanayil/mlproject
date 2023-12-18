
1) How to open our project in vscode in mac.
   
    a) open vscode
   
    b) select open folder

3) Create new environment
   
       a) In vscode terminal: conda create env_name (just a name) python==python_verson(mine 3.11) -y
   
   this will create a folder in our project folder, all packages will be added in this env_name folder.
   
       b) conda activate env_name/

6) Create a README.md file outside env_name

7) If git is never config before install git global config.(google it go to website do as give only need once in a system.)

8) set up github on local and do first push.
   
    a) follow below commands
   
        git init
        Create a readme
        git add README.md
        git commit -m "first commit"
        git branch -M main
        git remote add origin https://github.com/aakashpokkanayil/test.git  (new repo path)
        git push -u origin main

10) go to github repo(website) and create a new file there name: .gitignore
    
    a) select template dropdown as python and commit thr itself.
    
    its a file which contain list of file names which dont need to get commited.
    
    gitignore - Specifies intentionally untracked files to ignore


         11) git pull
    to pull all  data from git repo to local repo.


1) set up github.
  a) new envt.
  b) create setup.py
  c) create requirments.txt
