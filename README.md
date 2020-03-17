# Genetic_algorithm
Use genetic algorithm to fit the chrome icon.

## Main Python File
[Genetic.py](https://github.com/lxy764139720/Genetic_algorithm/blob/master/Genetic.py)

## Generated fiting images
generation+优(best)/中(mid)/差(worst).png

Each generation has 100 genes.Select the first,fiftieth,hundredth gene to generate the fiting picture.

## Fitness convergence curve
fitness+generation.png

## Gene encoding: multidimensional array
* The first dimension: [r,g,b,a],"a" is the sum of the absolute value of the difference between the three colors of RGB and the standard picture
* The second dimension: [rgba] list of 30 pixels per row
* The third dimension: a list of 30 rows
* The fourth dimension: a gene, the first value is a list of 30 by 30 pixels in an image, the second value is the fitness of the gene
* The fifth dimension: a list of 100 genes

## Method of gene selection: absolute value difference
Find the absolute value of the difference between the RGB value of each pixel and the standard image, and then add up the difference of all pixels in a picture.

Function:a=abs(target_r-r)+abs(target_g-g)+abs(target_b-b)

## Gene crossover mode: no crossover is used

## Gene variation strategy:
Each gene produces five offsprings, each of which takes the parent gene as a sample, with three levels of variation.

Variation mode 1: each RGB color was reselected with a probability of 0.05;

Variation mode 2: each RBG color fluctuates 30 units on the basis of the original value with a probability of 0.2.

Variation mode 3: each RBG color fluctuates 10 units on the basis of the original value with a probability of 0.5.

(Ensure that the RGB value after mutation is still between 0 and 255)

The fitness of the five offsprings is calculated and compared with that of the parent.
