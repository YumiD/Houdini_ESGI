#import du Module Houdini
import hou

#Création d’un objet
objets = hou.node('obj')

#Nettoyage de la scene
for node in objets.children():
    node.destroy()

#scene
scene = objets.createNode('geo','scene')

#Building
box = scene.createNode('box','building')
box.parm('ty').set(1.0)
box.parm('sizey').set(2.0)
TsolBox = scene.createNode('xform', 'TsolBox')
TsolBox.setInput(0,box)
colorBox = scene.createNode('color', 'colorBox')
colorBox.setInput(0,TsolBox)
colorBox.parm('colorr').set(0.6667)
colorBox.parm('colorg').set(0.6667)
colorBox.parm('colorb').set(0.6667)

#Arbre
tree = scene.createNode('lsystem','tree')
tree.parm('type').set("tube")
TsolTree = scene.createNode('xform', 'TsolTree')
TsolTree.setInput(0,tree)
colorTree = scene.createNode('color', 'colorTree')
colorTree.setInput(0,TsolTree)
colorTree.parm('colorr').set(0.3)
colorTree.parm('colorg').set(0.1875)
colorTree.parm('colorb').set(0.075)

#Rochers
rock = scene.createNode('metaball','rock')
rock.parm('expxy').set(1.6)
rock.parm('expz').set(2)
rock.parm('metaweight').set(1.5)
TsolRock = scene.createNode('xform', 'TsolRock')
TsolRock.setInput(0,rock)
colorRock = scene.createNode('color', 'colorRock')
colorRock.setInput(0,TsolRock)
colorRock.parm('colorr').set(0.333)
colorRock.parm('colorg').set(0.333)
colorRock.parm('colorb').set(0.333)

#Nuages
sphere = scene.createNode('sphere','sphere')
sphere.parm('radx').set(2.5)
sphere.parm('rady').set(0.6)
sphere.parm('radz').set(1.5)
sphere.parm('ty').set(6)
sphere.parm('scale').set(0.2)
TsolSphere = scene.createNode('xform', 'TsolSphere')
TsolSphere.setInput(0,sphere)
cloud = scene.createNode('cloud','cloud')
#cloud.parm('fillsourcegeo').set(True)
cloud.setInput(0,TsolSphere)
cloudNoise = scene.createNode('cloudnoise','cloudNoise')
cloudNoise.parm('noiseamount').set(0.2)
cloudNoise.setInput(0,cloud)

#Relions tous les élements
switch = scene.createNode('switch', 'switch')
switch.setInput(0,colorBox)
switch.setInput(1,colorTree)
switch.setInput(2,colorRock)
switch.setInput(3,cloudNoise)

#Sol
sol = scene.createNode('grid','sol')

#créer une dispersion scatter
points = scene.createNode('scatter::2.0', 'box_points')
#faire les liens entre les nodes (pour le scatter)
points.setInput(0,sol)

#For Each
forEach_begin = scene.createNode('block_begin', 'foreach_begin1' )
forEach_end = scene.createNode('block_end', 'foreach_end1')

forEach_begin.parm('method').set(1)
forEach_begin.parm('blockpath').set('../foreach_end1')
forEach_end.parm('blockpath').set('../foreach_begin1')
forEach_end.parm('templatepath').set('../foreach_begin1')
forEach_end.parm('method').set(1)

param_spare = switch.parmTemplateGroup()
my_parm = hou.StringParmTemplate(name='spare_input0', label='Spare input 0',num_components= 1, default_value = '')
param_spare.append(my_parm)

sort = scene.createNode('sort', 'sort')
sort.parm('ptsort').set(6)

wrangle = scene.createNode('attribwrangle', 'wrangle')
wrangle.parm('snippet').set('i@pt = @ptnum%4;')
wrangle.setInput (0,sort)
forEach_begin.setInput(0,wrangle)

switch.setParmTemplateGroup(param_spare)
switch.parm('spare_input0').set('../foreach_begin1')
switch.parm('input').setExpression('point(-1,0,"pt",0)')

#créer des copies d'objets sur les points
copy = scene.createNode('copytopoints::2.0', 'box_copy')
copy.setInput(0,switch)
copy.setInput(1,forEach_begin)
forEach_end.setInput(0,copy)

#Random sur le scale uniforme dans Houdini (pscale)
pRand = scene.createNode('attribrandomize', 'pRand')
pRand.setInput(0,points)
pRand.parm('name').set('pscale')
pRand.parm('minx').set(0.2)
pRand.parm('miny').set(0.2)
pRand.parm('minz').set(0.2)
pRand.parm('minw').set(0.2)

#Random sur la grille
gridScale = scene.createNode('xform', 'gridY')
gridScale.setInput(0, sol)
colorGrid = scene.createNode('color', 'colorBox')
colorGrid.setInput(0,gridScale)
colorGrid.parm('colorr').set(0.075)
colorGrid.parm('colorg').set(0.3)
colorGrid.parm('colorb').set(0.075)

#création d'un node de Relax
relax = scene.createNode('relax', 'pRelax')
relax.setInput(0,pRand)
relax.setInput(1,sol)
sort.setInput(0,relax)

#Fusionner mon arborescence
merge = scene.createNode('merge', 'solbox')
merge.setInput(0,forEach_end)
merge.setInput(1, colorGrid)

#Node de résultat de ma création
output = scene.createNode('null', 'output')
output.setInput(0,merge)

#---------------------------------------------
#Réglage des paramètres

#Choix du nombre de points
nbpoints = points.parm('npts')
nbpoints.set(80)

#---------------------------------------------
#Affichage

#gérer l’affichage des nodes
output.setDisplayFlag(True)
output.setRenderFlag(True)

#organiser les nodes
scene.layoutChildren()