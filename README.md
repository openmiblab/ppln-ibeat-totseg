# iBEAt-totseg

---
## Installation

Open Windows PowerShell

Go to the folder with the pipeline code:

```bash
cd C:\Users\md1spsx\Documents\GitHub\ppln-ibeat-totseg
```

If you have a previous installation, remove it first:

```bash
conda deactivate
conda env remove -n totseg
```

Then rinstall it again:

```bash
conda env create -f env.yml
```

and activate it:

```bash
conda activate -n totseg
```

## Starting a new session

Assuming the software environment is installed, open Windows 
PowerShell and go to the folder with the pipeline code:

```bash
cd C:\Users\md1spsx\Documents\GitHub\ppln-ibeat-totseg
```

Activate the environment
```bash
conda activate totseg
```

Define a data variable to point to the database for convenience:

```bash
$data = "C:\Users\md1spsx\Documents\Data\iBEAt_Build"
```

Note: Use Ctrl+C to interrupt calculations, but be aware this may corrupt the data you are writing

---

## Stage 1: Autosegmentation with TotalSegmentator

This has already been done - no need to run again.

---
## Stage 2: Build mosaic displays of autosegmented organs

Build mosaic displays of all organs:

```bash
python -m totseg.stage_2_display --build=$data
```

Build mosaic displays of aorta alone:

```bash
python -m totseg.stage_2_display --build=$data --organs aorta
```

Or multiple organs:

```bash
python -m totseg.stage_2_display --build=$data --organs aorta liver pancreas
```

---
## Stage 3: Measure autosegmented organs

Single organ:

```bash
python -m totseg.stage_3_measure --build=$data --organs aorta
```

Multiple organs:

```bash
python -m totseg.stage_3_measure --build=$data --organs aorta liver
```

All organs (THIS TAKES A LONG TIME!!!):

```bash
python -m totseg.stage_3_measure --build=$data
```

---
## Stage 4: Edit autosegmented masks


By default this is editing in the coronal plane, but you You MUST specify an organ to edit:

```bash
python -m totseg.stage_4_edit --build=$data --organ aorta
```

To edit in the axial plane:

```bash
python -m totseg.stage_4_edit --build=$data --organ aorta --plane axial
```

Or sagittal:

```bash
python -m totseg.stage_4_edit --build=$data --organ aorta --plane sagittal
```

---
## Stage 5: Build mosaic displays of edited organs

Build mosaic displays of all organs:

```bash
python -m totseg.stage_5_display --build=$data
```

Build mosaic displays of aorta alone:

```bash
python -m totseg.stage_5_display --build=$data --organs aorta
```

Or multiple organs:

```bash
python -m totseg.stage_5_display --build=$data --organs aorta liver pancreas
```

---
## Stage 6: Measure edited organs

Single organ:

```bash
python -m totseg.stage_5_measure --build=$data --organs aorta
```

Multiple organs:

```bash
python -m totseg.stage_5_measure --build=$data --organs aorta liver
```

All organs (THIS TAKES A LONG TIME!!!):

```bash
python -m totseg.stage_5_measure --build=$data
```
