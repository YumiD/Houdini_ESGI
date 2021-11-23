#import du Module Houdini
import hou

#Création d’un objet
objets = hou.node('obj')

#Nettoyage de la scene
for node in objets.children():
    node.destroy()

#scene
scene = objets.createNode('geo','scene')

#une box
box = scene.createNode('box','bloc')

#un sol
sol = scene.createNode('grid','sol')

#créer une dispersion scatter
points = scene.createNode('scatter::2.0', 'box_points')

#créer des copies d'objets sur les points
copy = scene.createNode('copytopoints::2.0', 'box_copy')

#faire les liens entre les nodes (pour le scatter)
points.setInput (0,sol)

#faire les liens pour la copy
#copy.setInput(0, box)
#copy.setInput(1,points)

#faire un node de transform
Tsol = scene.createNode('xform', 'Tsol')

#relions ce node aux bons nodes
Tsol.setInput(0,box)
copy.setInput(0,Tsol)

#Random sur le scale uniforme dans Houdini (pscale)
pRand = scene.createNode('attribrandomize', 'pRand')
pRand.setInput(0,points)

#Random sur la grille
gridScale = scene.createNode('xform', 'gridY')
gridScale.setInput(0, sol)

#création d'un node de Relax
relax = scene.createNode('relax', 'pRelax')
relax.setInput(0,pRand)
relax.setInput(1,sol)
copy.setInput(1,relax)

#Fusionner mon arborescence
merge = scene.createNode('merge', 'solbox')
merge.setInput(0,copy)
merge.setInput(1, gridScale)

#Node de résultat de ma création
output = scene.createNode('null', 'output')
output.setInput(0,merge)


#gérer l’affichage des nodes
output.setDisplayFlag(True)
output.setRenderFlag(True)

#organiser les nodes
scene.layoutChildren()

#-----------------------------
#Réglage des paramètres

#Choix du nombre de points
nbpoints = points.parm('npts')
nbpoints.set(50)

#Taille des box
box.parm('sizey').set(2.0)
