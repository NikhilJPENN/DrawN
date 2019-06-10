# DrawN

This is project for 
‘Interactive Freehand Sketching and Sketch Based Retrieval of 3D Object for Children’

his project follows traditional image classification and 3D model retrieval based on feature descriptors, mapping and matching approach. In this content based retrieval approach user can provide sketch as input query for retrieval of information. There are two methods in this category first one is purely based on geometric similarity between sketch and image content and another one learning the system and semantic understanding of the sketch.
(1) Construction of database. We select best suitable view points and 2D images of object. We generate line rendering or line drawing by applying canny edge detection on views/2D images. We then apply HOG descriptor to represent each image in database in terms of feature descriptor. (2) In second step, abstract user sketch is represented by HOG feature descriptor and the user sketch feature descriptor is compared with each line rendered feature descriptor to compute the similarity index using cosine distance. (3) Top 10 matches are selected on the basis of maximum similarity index. And finally 3D model is retrieved from database by selecting one of line rendering sketch in top 10 best matched line drawings.

Kindly look into DrawN.pdf

Kinldy look into drawN1.py

For full data set and other dependencies please contact! 
