# Cantera Workshop Materials

This repository has the Jupyter Notebooks and other materials used at Cantera workshops.

The URL of this site is: https://github.com/Cantera/workshop-materials

> [!NOTE]
> If you're attending the **2025 NCM Workshop**, you can find all relevant materials in the `ncm-2025` subfolder.

<!-- ## Installation Instructions

Please choose from the following list:

* [I do not have Python installed on my computer](#i-do-not-have-python-installed-on-my-computer)
* I already have Python installed on my computer
  * [I installed Python with Anaconda or Miniconda](#i-installed-python-with-anaconda-or-miniconda)
  * [I installed Python from https://python.org](#i-installed-python-from-the-official-site)

### I do not have Python installed on my computer

If you do not have Python or Cantera installed on your computer, we recommend that you use Anaconda or Miniconda to install Python. Anaconda and Miniconda are Python distributions that include the cross-platform `conda` package manager. This provides a consistent interface to install Python packages (including Cantera) whether you're running Windows, macOS, or Linux. The difference between Anaconda and Miniconda is that Anaconda includes a few hundred of the most commonly used Python packages in the installer along with Python and `conda`, while Miniconda includes just Python and `conda`. However, all the packages included with Anaconda are available to be installed within Miniconda.

* [Anaconda installer](https://www.anaconda.com/distribution/)
* [Miniconda installer](https://docs.conda.io/en/latest/miniconda.html)

Make sure to download the Python 3 version of the installer! Once you've installed Anaconda or Miniconda, open a terminal (on Linux or macOS) or the Anaconda Prompt (on Windows) and type

```console
conda update -n base conda
```

If this updates your version of conda, restart your terminal so that changes to your environment can take effect.
Then, follow the instructions directly below ("I installed Python with Anaconda or Miniconda") to install Cantera.

### I installed Python with Anaconda or Miniconda

Great! Now, you need to get the materials for the workshop. Head to <https://github.com/Cantera/workshop-materials> (you might already be reading this on that site) and find the "Clone or Download" button. If you have git installed on your computer, you can clone the repository. If you don't, or don't know what cloning means, don't worry! Click the green button, then click "Download ZIP", as shown in the picture below:

![Download a Zip of the repository](./images/download-repo-zip.png)

Once the zip file finishes downloading, unzip it and remember where the files are.

Open your terminal (Linux or macOS) or the Anaconda Prompt (Windows) and use the `cd` command to change into the directory with the files you just cloned/unzipped. For instance, if you unzipped the files into your `Downloads` folder, then the command will look like:

```console
cd Downloads/workshop-materials
```

Now you need to create a conda environment with all of the Python packages you will need.

```console
conda env create -f environment.yml
```

Finally, to run the files for the Workshop, in the same Anaconda Prompt or terminal window, activate the newly created environment and start a Jupyter Notebook server by typing

```console
conda activate ct-workshop
jupyter notebook
```

This should automatically open a page in your web browser that shows you the files for the Workshop. We're going to be working from one of the sub-folders in the zip file.

Hooray! You're all set! See you on Sunday!

### I installed Python from the official site

If you installed Python from <https://python.org>, you will need to follow the [operating system-specific instructions](https://cantera.org/install) for your platform to install Cantera.

If you're on macOS, the instructions have you use Miniconda to install Cantera anyways, so you should head on up to the [I do not have Python installed on my computer](#i-do-not-have-python-installed-on-my-computer) instructions.

If you're on Windows, we do have a separate installer for the python.org version of Python. Head over to the Cantera website and check out the appropriate instructions: [Windows](https://cantera.org/install/windows-install.html)

Once you've got Cantera installed, you'll need to install a few other dependencies. Open a command prompt and type:

```console
py -m pip install pandas matplotlib notebook scipy
```

Now, you need to get the materials for the workshop. Head to <https://github.com/Cantera/workshop-materials> (you might already be reading this on that site) and find the "Clone or Download" button. If you have git installed on your computer, you can clone the repository. If you don't, or don't know what cloning means, don't worry! Click the green button, then click "Download ZIP", as shown in the picture below:

![Download a Zip of the repository](./images/download-repo-zip.png)

Once the zip file finishes downloading, unzip it and remember where the files are.

Open your terminal (Linux or macOS) or the Anaconda Prompt (Windows) and use the `cd` command to change into the directory with the files you just cloned/unzipped. For instance, if you unzipped the files into your `Downloads` folder, then the command will look like:

```console
cd Downloads/workshop-materials
```

Finally, to run the files for the Workshop start a Jupyter Notebook server by typing:

```console
jupyter notebook
```

This should automatically open a page in your web browser that shows you the files for the Workshop. We're going to be working from one of the sub-folders in the zip file.

Hooray! You're all set! See you on Sunday!-->
