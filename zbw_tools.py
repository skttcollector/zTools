########################
# file: zbw_tools.py
# Author: zeth willie
# Contact: zethwillie@gmail.com, www.williework.blogspot.com
# Date Modified: 8/17/17
# To Use: type in python window  "import zbw_tools as tools; reload(tools); tools.tools()"
# Notes/Descriptions: some rigging, anim, modeling and shading tools. *** requires zTools folder in a python path.
########################

# todo: maybe add space buffer?
# todo: deformer weights
# todo: drop in all mel scripts deal with sourceing mel scripts from zTools (comet, etc with attribution), brave rabbit
# TODO add some tooltips to buttons
# Todo - add docs to all of these
# todo maybe add shader/uv transfer to rig?
# TODo move the dictionary to resources and pull it from there

from functools import partial
import os
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om

import zTools.rig.zbw_rig as rig
reload(rig)
import zTools.resources.zbw_pipe as pipe
reload(pipe)
import zTools.resources.zbw_removeNamespaces as rmns

widgets = {}

# make sure maya can see and call mel scripts from zTools (where this is called from)
zToolsPath = os.path.dirname(os.path.abspath(__file__))
subpaths = ["", "rig", "resources", "anim", "model", "shaderRender"]
newPaths = []
for p in subpaths:
    thisPath = os.path.join(zToolsPath, p)
    newPaths.append(thisPath)

# set up these zTools paths for maya to recognize mel scripts
pipe.add_maya_script_paths(newPaths)

zRigDict = {
    "attr": "import zTools.rig.zbw_attributes as zat; reload(zat); zat.attributes()",
    "snap": "import zTools.rig.zbw_snap as snap; reload(snap), snap.snap()",
    "shpScl": "import zTools.rig.zbw_shapeScale as zss; zss.shapeScale()",
    "selBuf": "import zTools.rig.zbw_selectionBuffer as buf; reload(buf); buf.selectionBuffer()",
    "smIK": "import zTools.rig.zbw_smallIKStretch as zsik; zsik.smallIKStretch()",
    "foll": "import zTools.rig.zbw_makeFollicle as zmf; reload(zmf); zmf.makeFollicle()",
    "ribbon": "import zTools.rig.zbw_ribbon as zrib; reload(zrib); zrib.ribbon()",
    "soft": "import zTools.rig.zbw_softDeformer as zsft; reload(zsft); zsft.softDeformer()",
    "jntRadius": "import zTools.rig.zbw_jointRadius as jntR; jntR.jointRadius()",
    "cmtRename": "mel.eval('cometRename')",
    "trfmBuffer": "import zTools.rig.zbw_transformBuffer as ztbuf; reload(ztbuf); ztbuf.transformBuffer()",
    "crvTools": "import zTools.rig.zbw_curveTools as ctool; reload(ctool); ctool.curveTools()",
    "abSym": "mel.eval('abSymMesh')",
    "cmtJntOrnt": "mel.eval('cometJointOrient')",
    "autoSquash": "import zTools.rig.zbw_autoSquashRig as zAS; reload(zAS); zAS.autoSquashRig()",
    "BSpirit": "mel.eval('BSpiritCorrectiveShape')",
    "follow": "import zTools.rig.zbw_followConstraints as zFC; reload(zFC); zFC.followConstraints()",
    "splineIK": "import zTools.rig.zbw_splineRig as zspik; reload(zspik); zspik.splineRig()",
    "leg": "import zTools.rig.auto_legRig as leg; reload(leg); LEG=leg.LegRigUI()",
    "arm": "import zTools.rig.auto_armRig as arm; reload(arm); ARM = arm.ArmRigUI()",
    "typFind": "import zTools.rig.zbw_typeFinder as zType; reload(zType); zType.typeFinder()",
    "wire": "import zTools.rig.zbw_wireRig as wire; reload(wire); wire.wireRig()",
    "sphereCrvRig":"import zTools.rig.zbw_sphereCrvRig as zscr; reload(zscr); zscr.sphereCrvRig()",
}

zAnimDict = {
    "tween": "import zTools.anim.tweenMachine as tm; tm.start()",
    "noise": "import zTools.anim.zbw_animNoise as zAN; reload(zAN); zAN.animNoise()",
    "audio": "import zTools.anim.zbw_audioManager as zAM; reload(zAM); zAM.audioManager()",
    "clean": "import zTools.anim.zbw_cleanKeys as zCK; reload(zCK); zCK.cleanKeys()",
    "dupe": "import zTools.anim.zbw_dupeSwap as zDS; reload(zDS);zDS.dupeSwap()",
    "huddle": "import zTools.anim.zbw_huddle as zH; reload(zH);zH.huddle()",
    "randomSel": "import zTools.anim.zbw_randomSelection as zRS; reload(zRS);zRS.randomSelection()",
    "randomAttr": "import zTools.anim.zbw_randomAttrs as zRA; reload(zRA); zRA.randomAttrs()",
    "clip": "import zTools.anim.zbw_setClipPlanes as zSC; reload(zSC); zSC.setClipPlanes()",
    "tangents": "import zTools.anim.zbw_tangents as zTan; reload(zTan); zTan.tangents()"
}

zModelDict = {
    "extend": "import zTools.model.zbw_polyExtend as zPE; reload(zPE); zPE.polyExtend()",
    "wrinkle": "import zTools.model.zbw_wrinklePoly as zWP; reload(zWP); zWP.wrinklePoly()"
}

zShdDict = {
    "shdTransfer": "import zTools.shaderRender.zbw_shadingTransfer as zST; reload(zST); zST.shadingTransfer()"
}

colors = rig.colors

def tools_UI(*args):
    if cmds.window("toolsWin", exists=True):
        cmds.deleteUI("toolsWin")

    widgets["win"] = cmds.window("toolsWin", t="zTools", w=280, rtf=True,
                                 s=True)
    widgets["tab"] = cmds.tabLayout(w=280)
    widgets["rigCLO"] = cmds.columnLayout("TD", w=280)
    widgets["rigFLO"] = cmds.formLayout(w=280, bgc=(0.1, 0.1, 0.1))

    # controls layout
    widgets["ctrlFLO"] = cmds.formLayout(w=270, h=50, bgc=(0.3, 0.3, 0.3))
    widgets["ctrlFrLO"] = cmds.frameLayout(l="CONTROLS", w=270, h=50, bv=True,bgc=(0.0, 0.0, 0.0))
    widgets["ctrlInFLO"] = cmds.formLayout(bgc=(0.3, 0.3, 0.3))
    widgets["ctrlAxisRBG"] = cmds.radioButtonGrp(l="Axis", nrb=3, la3=("x", "y", "z"),cw=([1, 33], [2, 33], [3, 33]),cal=([1, "left"], [2, "left"],[3, "left"]), sl=1)
    widgets["ctrlBut"] = cmds.button(l="Create Control", w=100, bgc=(.7,.7,.5))
    cmds.popupMenu(b=1)
    cmds.menuItem(l="circle", c=partial(control, "circle"))
    cmds.menuItem(l="sphere", c=partial(control, "sphere"))
    cmds.menuItem(l="square", c=partial(control, "square"))
    cmds.menuItem(l="cube", c=partial(control, "cube"))
    cmds.menuItem(l="lollipop", c=partial(control, "lollipop"))
    cmds.menuItem(l="barbell", c=partial(control, "barbell"))
    cmds.menuItem(l="cross", c=partial(control, "cross"))
    cmds.menuItem(l="bentCross", c=partial(control, "bentCross"))
    cmds.menuItem(l="arrow", c=partial(control, "arrow"))
    cmds.menuItem(l="bentArrow", c=partial(control, "bentArrow"))
    cmds.menuItem(l="arrowCross", c=partial(control, "arrowCross"))
    cmds.menuItem(l="splitCircle", c=partial(control, "splitCircle"))
    cmds.menuItem(l="cylinder", c=partial(control, "cylinder"))
    cmds.menuItem(l="octagon", c=partial(control, "octagon"))
    cmds.menuItem(l="halfCircle", c=partial(control, "halfCircle"))
    cmds.menuItem(l="arrowCircle", c=partial(control, "arrowCircle"))
    cmds.menuItem(l="arrowSquare", c=partial(control, "arrowSquare"))
    cmds.menuItem(l="4ArrowSquare", c=partial(control, "4arrowSquare"))
    cmds.menuItem(l="MASTER PACK", c=create_master_pack)

    cmds.formLayout(widgets["ctrlInFLO"], e=True, af=[
        (widgets["ctrlAxisRBG"],"left", 0),
        (widgets["ctrlAxisRBG"], "top", 0),
        (widgets["ctrlBut"], "left", 170),
        (widgets["ctrlBut"], "top", 0),
    ])
    # TODO - add scale factor field for control creation

    # action layout
    cmds.setParent(widgets["rigFLO"])
    widgets["actionFLO"] = cmds.formLayout(w=280, h=330, bgc=(0.3, 0.3, 0.3))
    widgets["actionFrLO"] = cmds.frameLayout(l="ACTIONS", w=280, h=330, bv=True, bgc=(0, 0, 0))
    widgets["actionRCLO"] = cmds.rowColumnLayout(bgc=(0.3, 0.3, 0.3), nc=2)
    widgets["grpFrzBut"] = cmds.button(l="group freeze selected", w=140, bgc=(.5, .7, .5), c=group_freeze)
    widgets["grpAbvBut"] = cmds.button(l="insert group above ('Grp')", w=140, bgc=(.5, .7, .5), c=insert_group_above)
    widgets["grpCnctBut"] = cmds.button(l="group freeze + connect", w=140, bgc=(.5, .7, .5), c=freeze_and_connect)
    widgets["slctHiBut"] = cmds.button(l="select hierarchy", w=140, bgc=(.5, .7, .5), c=select_hi)
    widgets["prntChnBut"] = cmds.button(l="parent chain selected", w=140, bgc=(.5, .7, .5), c=parent_chain)
    widgets["hideShp"] = cmds.button(l="sel shape vis toggle", w=140, bgc=(.5, .7, .5), c=hide_shape)
    widgets["bBox"] = cmds.button(l="bounding box control", w=140, bgc=(.5, .7, .5), c=bBox)
    widgets["cpSkinWtsBut"] = cmds.button(l="copy skin & weights", w=140, bgc=(.5, .7, .5), c=copy_skinning)
    widgets["remNSBut"] = cmds.button(l="remove all namespaces", w=140, bgc=(.5, .7, .5), c=remove_namespace)
    widgets["cntrLoc"] = cmds.button(l="sel vtx cntr jnt", w=140,bgc=(.5, .7, .5), c=center_joint)
    widgets["addToLat"] = cmds.button(l="add to lattice", w=140, bgc=(.5, .7, .5), c=add_lattice)
    widgets["snapto"] = cmds.button(l="snap B to A", w=140, bgc=(.5, .7, .5),c=snap_b_to_a)
    widgets["sclPrntCnstr"] = cmds.button(l="Parent+Scl Constrain", w=140, bgc=(.5, .7, .5),c=parent_scale_constrain)
    widgets["zeroPiv"] = cmds.button(l="Zero Pivot", w=140, bgc=(.5, .7, .5),c=zero_pivot)
    widgets["centerPiv"] = cmds.button(l="Center Pivot", w=140, bgc=(.5, .7, .5), c=center_pivot)
    widgets["setBut"] = cmds.button(l="Create Set", w=140, bgc=(.5, .7, .5), c=rig.create_set)
    widgets["clnJntBut"] = cmds.button(l="Scrub Jnt Chain", w=140, bgc=(.5, .7, .5), c=clean_joints)
    widgets["jntTool"] = cmds.button(l="Create Joint", w=140, bgc=(.5, .7, .5), c=create_joint)
    widgets["hmmrBut"] = cmds.button(l="Hammer Weights", w=140, bgc=(.5, .7, .5), c=hammer_skin_weights)
    widgets["locatorBut"] = cmds.button(l="Create Locator", w=140, bgc=(.5, .7, .5), c=create_locator)

    cmds.rowColumnLayout(w=140, nc=2, cs=[(1, 5), (2,5)])
    widgets["deleteH"] = cmds.button(l="del hist", w=65, bgc=(.7, .7, .5), c=partial(deleteH, 0))
    widgets["deleteAnim"] = cmds.button(l="del Anim", w=65, bgc=(.7, .5, .5), c=partial(deleteH, 1))
    cmds.setParent(widgets["actionRCLO"])

    cmds.rowColumnLayout(w=140, nc=4, cs=[(1, 5), (2,5), (3,5), (4,5)])
    cmds.text("Freeze: ")
    widgets["freezeT"] = cmds.button(l="T", w=23, bgc=(.7, .5, .5), c=partial(freeze, 1, 0, 0))
    widgets["freezeR"] = cmds.button(l="R", w=23, bgc=(.5, .7, .5), c=partial(freeze, 0, 1, 0))
    widgets["freezeS"] = cmds.button(l="S", w=23, bgc=(.5, .5, .7), c=partial(freeze, 0, 0, 1))
    cmds.setParent(widgets["actionRCLO"])

    cmds.rowColumnLayout(w=140, nc=3, cs=[(1, 5), (2,10), (3, 5)])
    cmds.text("Curve Thick")
    widgets["linThkBut"] = cmds.button(l="-", w=30, bgc=(.7, .5, .5), c=partial(line_width, 0))
    widgets["linThnBut"] = cmds.button(l="+", w=30, bgc=(.5, .7, .5), c=partial(line_width, 1))
    cmds.setParent(widgets["actionRCLO"])

    cmds.rowColumnLayout(w=140, nc=3, cs=[(1, 5), (2,5), (3, 5)])
    cmds.text("Joint Draw ")
    widgets["jntDrwOn"] = cmds.button(l="off", w=30, bgc=(.7, .5, .5), c=partial(joint_draw, 2))
    widgets["jntDrwOff"] = cmds.button(l="on", w=30, bgc=(.5, .7, .5), c=partial(joint_draw, 0))
    cmds.setParent(widgets["actionRCLO"])

    cmds.rowColumnLayout(w=140, nc=3, cs=[(1, 5), (2,17), (3, 5)])
    cmds.text("Joint Size ")
    widgets["jntSizeUp"] = cmds.button(l="-", w=30, bgc=(.7, .5, .5), c=partial(size_joints, 0))
    widgets["jntSizeDn"] = cmds.button(l="+", w=30, bgc=(.5, .7, .5), c=partial(size_joints, 1))
    cmds.setParent(widgets["actionRCLO"])

    cmds.rowColumnLayout(w=140, nc=3, cs=[(1, 5), (2,8), (3, 5)])
    cmds.text("LocRotAxis")
    widgets["lraOff"] = cmds.button(l="off", w=30, bgc=(.7, .5, .5), c=partial(lra_toggle, 0))
    widgets["lraOn"] = cmds.button(l="on", w=30, bgc=(.5, .7, .5), c=partial(lra_toggle, 1))
    cmds.setParent(widgets["actionRCLO"])

    cmds.setParent(widgets["actionRCLO"])

#TODO---------------- grp freeze and connect should replicate the hierarchy

#TODO -- add hide ai attributes
# todo - group freeze connect AND parent ctrls into a hierarchy
# todo - group freeze should leave object in place in hierarchy?

    # script Layout
    cmds.setParent(widgets["rigFLO"])
    widgets["zScrptFLO"] = cmds.formLayout(w=280, bgc=(0.3, 0.3, 0.3))
    widgets["zScrptFrLO"] = cmds.frameLayout(l="SCRIPTS", w=280, bv=True, bgc=(0.0, 0.0, 0.0))
    widgets["rigScriptsRCLO"] = cmds.rowColumnLayout(w=280, nc=2)
    widgets["attrBut"] = cmds.button(l="zbw_attrs", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict, "attr"))
    widgets["shpSclBut"] = cmds.button(l="zbw_shapeScale", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict,"shpScl"))
    widgets["selBufBut"] = cmds.button(l="zbw_selectionBuffer", w=140,bgc=(.7, .5, .5), c=partial(zAction, zRigDict,"selBuf"))
    widgets["snapBut"] = cmds.button(l="zbw_snap", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict, "snap"))
    widgets["follBut"] = cmds.button(l="zbw_makeFollicle", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict,"foll"))
    widgets["jntRadBut"] = cmds.button(l="zbw_jointRadius", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict,"jntRadius"))
    widgets["typFindBut"] = cmds.button(l="zbw_typeFinder", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict,"typFind"))
    widgets["cmtRename"] = cmds.button(l="cometRename", w=140, bgc=(.5, .5, .5), c=partial(zAction, zRigDict, "cmtRename"))
    widgets["abSym"] = cmds.button(l="abSymMesh", w=140, bgc=(.5, .5, .5), c=partial(zAction, zRigDict,"abSym"))
    widgets["cmtJntOrnt"] = cmds.button(l="cometJntOrient", w=140, bgc=(.5, .5, .5), c=partial(zAction, zRigDict,"cmtJntOrnt"))
    widgets["BSpirit"] = cmds.button(l="BSpirtCorrective", w=140, bgc=(.5, .5, .5), c=partial(zAction, zRigDict,"BSpirit"))
    widgets["extract"] = cmds.button(l="Extract Deltas", w=135, bgc=(.5, .5,
                                                                     .5),)
    # color layout
    cmds.setParent(widgets["rigFLO"])
    widgets["colorFLO"] = cmds.formLayout(w=280, h=66, bgc=(0.3, 0.3, 0.3))
    widgets["colorFrLO"] = cmds.frameLayout(l="COLORS", w=280, h=66, bv=True, bgc=(0.0, 0.0, 0.0))
    widgets["colorRCLO"] = cmds.rowColumnLayout(nc=6)
    widgets["redCNV"] = cmds.canvas(w=48, h=20, rgb=(1, 0, 0), pc=partial(changeColor, colors["red"]))
    widgets["pinkCNV"] = cmds.canvas(w=48, h=20, rgb=(1, .8, .965), pc=partial(changeColor, colors["pink"]))
    widgets["blueCNV"] = cmds.canvas(w=48, h=20, rgb=(0, 0, 1), pc=partial(changeColor, colors["blue"]))
    widgets["ltBlueCNV"] = cmds.canvas(w=48, h=20, rgb=(.65, .8, 1), pc=partial(changeColor, colors["lightBlue"]))
    widgets["greenCNV"] = cmds.canvas(w=48, h=20, rgb=(0, 1, 0), pc=partial(changeColor, colors["green"]))
    widgets["dkGreenCNV"] = cmds.canvas(w=48, h=20, rgb=(0, .35, 0), pc=partial(changeColor, colors["darkGreen"]))
    widgets["yellowCNV"] = cmds.canvas(w=48, h=20, rgb=(1, 1, 0), pc=partial(changeColor, colors["yellow"]))
    widgets["brownCNV"] = cmds.canvas(w=48, h=20, rgb=(.5, .275, 0), pc=partial(changeColor, colors["brown"]))
    widgets["purpleCNV"] = cmds.canvas(w=48, h=20, rgb=(.33, 0, .33), pc=partial(changeColor, colors["purple"]))
    widgets["dkPurpleCNV"] = cmds.canvas(w=48, h=20, rgb=(.15, 0, .25), pc=partial(changeColor, colors["darkPurple"]))
    widgets["dkRedCNV"] = cmds.canvas(w=48, h=20, rgb=(.5, .0, 0), pc=partial(changeColor, colors["darkRed"]))
    widgets["ltBrownCNV"] = cmds.canvas(w=48, h=20, rgb=(.7, .5, .0), pc=partial(changeColor, colors["lightBrown"]))
# ---------------- add three more colors
    # formlayout stuff
    cmds.formLayout(widgets["rigFLO"], e=True, af=[
        (widgets["ctrlFLO"], "left", 0),
        (widgets["ctrlFLO"], "top", 0),
        (widgets["actionFLO"], "left", 0),
        (widgets["actionFLO"], "top", 50),
        (widgets["zScrptFLO"], "left", 0),
        (widgets["zScrptFLO"], "top", 457),
        (widgets["colorFLO"], "left", 0),
        (widgets["colorFLO"], "top", 385),
    ])

    cmds.setParent(widgets["tab"])
    widgets["rigsCLO"] = cmds.columnLayout("RIGS", w=280)
    widgets["rigsPropFrameLO"] = cmds.frameLayout(l="PROP RIGGING", w=280, bv=True, bgc=(0, 0, 0))
    widgets["rigsPropRCLO"] = cmds.rowColumnLayout(nc=2, bgc=(0.3, 0.3, 0.3))
    widgets["sftDefBut"] = cmds.button(l="Soft Deformers", w=140, bgc=(.5, .7, .5), c=partial(zAction,zRigDict,"soft"))
    widgets["RcrvTools"] = cmds.button(l="Curve Tools", w=140, bgc=(.5, .7, .5), c=partial(zAction, zRigDict, "crvTools"))
    widgets["smIKBut"] = cmds.button(l="Single Jnt IK", w=140, bgc=(.5, .7, .5), c=partial(zAction, zRigDict,"smIK"))
    widgets["autoSqBut"] = cmds.button(l="AutoSquash Rig", w=140, bgc=(.5, .7, .5), c=partial(zAction, zRigDict,"autoSquash"))
    widgets["wireBut"] = cmds.button(l="Wire Def Rig", w=140, bgc=(.5, .7, .5), c=partial(zAction, zRigDict, "wire"))
    cmds.setParent(widgets["rigsCLO"])
    widgets["rigsCharFrameLO"] = cmds.frameLayout(l="CHARACTER RIGGING", w=280, bv=True, bgc=(0, 0, 0))
    widgets["rigsCharRCLO"] = cmds.rowColumnLayout(nc=2, bgc=(0.3, 0.3, 0.3))
    widgets["legBut"] = cmds.button(l="Leg Rig", w=140, bgc=(.5, .7, .5), c=partial(zAction, zRigDict,"leg"))
    widgets["armBut"] = cmds.button(l="Arm Rig", w=140, bgc=(.5, .7, .5), c=partial(zAction, zRigDict, "arm"))
    cmds.setParent(widgets["rigsCLO"])
    widgets["rigsCharTFrameLO"] = cmds.frameLayout(l="CHARACTER TOOLS", w=280, bv=True, bgc=(0, 0, 0))
    widgets["rigsCharTRCLO"] = cmds.rowColumnLayout(nc=2, bgc=(0.3, 0.3, 0.3))
    widgets["ribBut"] = cmds.button(l="Ribbon Rig", w=140, bgc=(.5, .7, .5), c=partial(zAction, zRigDict,"ribbon"))
    widgets["splineBut"] = cmds.button(l="Spline IK Rig", w=140, bgc=(.5, .7, .5), c=partial(zAction, zRigDict, "splineIK"))
    widgets["followBut"] = cmds.button(l="Follow Constraints", w=140, bgc=(.5, .7, .5), c=partial(zAction, zRigDict,"follow"))
    widgets["mgRig"] = cmds.button(l="spherical Crv Rig", w=140, bgc=(.5, .7, .5), c=partial(zAction, zRigDict, "sphereCrvRig"))


    cmds.setParent(widgets["tab"])
    widgets["modelCLO"] = cmds.columnLayout("MDL", w=280)
# curve tools, model scripts, add to lattice, select hierarchy, snap selection buffer, transform buffer
    widgets["MaddToLat"] = cmds.button(l="add to lattice", w=140, bgc=(.5, .7, .5), c=add_lattice)
    widgets["extend"] = cmds.button(l="zbw_polyExtend", w=140, bgc=(.7, .5, .5),c=partial(zAction, zModelDict,"extend"))
    widgets["wrinkle"] = cmds.button(l="zbw_wrinklePoly", w=140, bgc=(.7, .5, .5), c=partial(zAction, zModelDict,"wrinkle"))
    widgets["McrvTools"] = cmds.button(l="zbw_curveTools", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict, "crvTools"))
    widgets["MtrnBuffer"] = cmds.button(l="zbw_transformBuffer", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict, "trfmBuffer"))
    widgets["MrandomSel"] = cmds.button(l="zhw_randomSel", w=140, bgc=(.7, .5, .5), c=partial(zAction, zAnimDict,"randomSel"))
    widgets["MselBufBut"] = cmds.button(l="zbw_selectionBuffer", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict,"selBuf"))
    widgets["MsnapBut"] = cmds.button(l="zbw_snap", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict, "snap"))
    widgets["MabSym"] = cmds.button(l="abSymMesh", w=140, bgc=(.5, .5, .5), c=partial(zAction, zRigDict,"abSym"))
    widgets["McmtRename"] = cmds.button(l="cometRename", w=140, bgc=(.5, .5, .5), c=partial(zAction, zRigDict,"cmtRename"))
    widgets["cube"] = cmds.button(l="zeroed cube", w=140, bgc=(.5, .5, .5))
    widgets["cylinder"] = cmds.button(l="zeroed cylinder", w=140, bgc=(.5, .5, .5))

    cmds.setParent(widgets["tab"])
    widgets["animCLO"] = cmds.columnLayout("ANIM", w=280)
    widgets["tween"] = cmds.button(l="tween machine", w=140, bgc=(.5, .5, .5), c=partial(zAction, zAnimDict, "tween"))
    widgets["noise"] = cmds.button(l="zbw_animNoise", w=140, bgc=(.7, .5, .5), c=partial(zAction, zAnimDict, "noise"))
    widgets["audio"] = cmds.button(l="zbw_audioManager", w=140, bgc=(.7, .5, .5),c=partial(zAction, zAnimDict, "audio"))
    widgets["clean"] = cmds.button(l="zbw_cleanKeys", w=140, bgc=(.7, .5, .5), c=partial(zAction, zAnimDict, "clean"))
    widgets["dupe"] = cmds.button(l="zbw_dupeSwap", w=140, bgc=(.7, .5, .5), c=partial(zAction, zAnimDict, "dupe"))
    widgets["huddle"] = cmds.button(l="zbw_huddle", w=140, bgc=(.7, .5, .5), c=partial(zAction, zAnimDict,"huddle"))
    widgets["randomSel"] = cmds.button(l="zhw_randomSel", w=140, bgc=(.7, .5, .5),c=partial(zAction, zAnimDict,"randomSel"))
    widgets["randomAttr"] = cmds.button(l="zbw_randomAttr", w=140, bgc=(.7, .5, .5),c=partial(zAction, zAnimDict,"randomAttr"))
    widgets["clip"] = cmds.button(l="zbw_setClipPlanes", w=140, bgc=(.7, .5, .5), c=partial(zAction, zAnimDict,"clip"))
    widgets["tangents"] = cmds.button(l="zbw_tangents", w=140, bgc=(.7, .5, .5), c=partial(zAction, zAnimDict, "tangents"))
    widgets["studLib"] = cmds.button(l="Studio Library", w=140, bgc=(.5, .7,.5))
    widgets["atools"] = cmds.button(l="ATools", w=140, bgc=(.5, .7,.5))
    widgets["picker"] = cmds.button(l="Anim School Picker", w=140, bgc=(.5, .7,.5),)

    cmds.setParent(widgets["tab"])
    widgets["lgtRndCLO"] = cmds.columnLayout("LT_RN", w=280)
    widgets["transfer"] = cmds.button(l="zbw_shadingTransfer", w=140, bgc=(.7, .5, .5), c=partial(zAction, zShdDict, "shdTransfer"))

    cmds.setParent(widgets["tab"])
    widgets["lgtRndCLO"] = cmds.columnLayout("MISC", w=280)
    widgets["saveScrpt"] = cmds.button(l="save script win", w=140, bgc=(.7, .5, .5), c=save_script_win)
    widgets["monWin"] = cmds.button(l="window cleanup", w=140, bgc=(.7, .5, .5))



    cmds.window(widgets["win"], e=True, rtf=True, w=5, h=5)
    cmds.showWindow(widgets["win"])

##########
# functions
##########

def control(type="none", *args):
    """
    gets the name from the button pushed and the axis from the radio button group
    and creates a control at the origin
    """
    axisRaw = cmds.radioButtonGrp(widgets["ctrlAxisRBG"], q=True, sl=True)
    if axisRaw == 1:
        axis = "x"
    if axisRaw == 2:
        axis = "y"
    if axisRaw == 3:
        axis = "z"

    rig.create_control(name="Ctrl", type=type, axis=axis, color="yellow")


def zAction(dict=None, action=None, *args):
    """
    grabs the action key from the given dictionary and executes that value
    """
    if action and dict:
        x = dict[action]
        print "executing: {}".format(x)
        exec (x)

    else:
        cmds.warning(
            "zbw_tools.zAction: There was a problem with either the key or the dictionary given! (key: {0}, "
            "action: {1}".format(action, dict))


def snap_b_to_a(*args):
    """
    snaps 2nd selection to 1st, translate and rotate. Transforms only
    """
    sel = cmds.ls(sl=True, type="transform")
    if sel and len(sel) > 1:
        src = sel[0]
        tgt = sel[1:]
        for t in tgt:
            rig.snap_to(src, t)


def zero_pivot(*args):
    """puts pivots zeroed at origin"""
    sel = cmds.ls(sl=True, transforms=True)
    rig.zero_pivot(sel)


def clean_joints(*args):
    sel = cmds.ls(sl=True, type="joint")
    if sel:
        jnt = sel[0]
        rig.clean_joint_chain(jnt)
        cmds.joint(jnt, edit=True, orientJoint="xyz", secondaryAxisOrient="yup", ch=True)


def freeze(t=1, r=1, s=1, *args):
    sel = cmds.ls(sl=True)
    cmds.makeIdentity(sel, t=t, r=r, s=s, apply=True )


def deleteH(mode, *args):
    sel = cmds.ls(sl=True)
    if mode == 0:
        cmds.delete(sel, ch=True)
    else:
        cmds.delete(sel, c=True, timeAnimationCurves=True, unitlessAnimationCurves=False)


def save_script_win(*args):
    mel.eval("syncExecuterBackupFiles")


def line_width(mode, *args):
    sel = cmds.ls(sl=True)
    if sel:
        for obj in sel:
            if rig.type_check(obj, "nurbsCurve"):
                shps = cmds.listRelatives(obj, s=True)
                if shps:
                    for shp in shps:
                        print shp
                        val = cmds.getAttr("{0}.lineWidth".format(shp))
                        if mode == 0:
                            if val <= 1:
                                continue
                            else:
                                val -= 0.5
                        elif mode == 1:
                            if val <= 1:
                                val = 1.5
                            else:
                                val += 0.5
                        print "final val:", val
                        cmds.setAttr("{0}.lineWidth".format(shp), val)


def joint_draw(value, *args):
    jnts = cmds.ls(type="joint")
    for jnt in jnts:
        cmds.setAttr("{0}.drawStyle".format(jnt), value)


def size_joints(mode, *args):
    jnts = cmds.ls(type="joint")
    for jnt in jnts:
        jntRad = cmds.getAttr("{0}.radius".format(jnt))
        if mode == 0:
            jntRad *= 0.5
        elif mode == 1:
            jntRad *= 1.5

        if jntRad < 0.01:
            jntRad = 0.01
        cmds.setAttr("{0}.radius".format(jnt), jntRad)


def lra_toggle(value, *args):
    sel = cmds.ls(sl=True)
    for obj in sel:
        cmds.setAttr("{0}.displayLocalAxis".format(obj), value)


def center_pivot(*args):
    sel = cmds.ls(sl=True)
    for obj in sel:
        cmds.xform(obj, cp=True, p=True)


def create_joint(*args):
    cmds.select(cl=True)
    cmds.joint()


def create_master_pack(self):
    mst1 = rig.create_control(name="master_CTRL", type="arrowCircle", axis="y", color = "green")
    mst2 = rig.create_control(name="master_sub1_CTRL", type="circle", axis = "y", color = "darkGreen")
    mst2Grp = rig.group_freeze(mst2)
    mst3 = rig.create_control(name="master_sub2_CTRL", type="circle", axis = "y", color = "yellowGreen")
    mst3Grp = rig.group_freeze(mst3)

    rig.scale_nurbs_control(mst1, 3, 3, 3, origin=True)
    rig.scale_nurbs_control(mst2, 2.5, 2.5, 2.5)
    rig.scale_nurbs_control(mst3, 2, 2, 2)

    cmds.parent(mst3Grp, mst2)
    cmds.parent(mst2Grp, mst1)


def parent_scale_constrain(*args):
    """ just creates a parent and scale transform on the tgt object """
    sel = cmds.ls(sl=True, type="transform")
    if not (sel and len(sel) == 2):
        cmds.warning("You need to select two tranform objects!")
        return ()
    src = sel[0]
    tgt = sel[1]
    cmds.parentConstraint(src, tgt, mo=True)
    cmds.scaleConstraint(src, tgt)


def remove_namespace(*args):
    """removes namespaces . . . """
    ns = rmns.remove_namespaces()
    if ns:
        print "Removed namespaces: ", ns
    else:
        print "Did not delete any namespaces!"


def add_lattice(*args):
    """
    select lattice then geo to add to the lattice
    """
    sel = cmds.ls(sl=True)
    lat = sel[0]
    geo = sel[1:]
    rig.add_to_lattice(lat, geo)


def group_freeze(*args):
    """group freeze an obj"""

    sel = cmds.ls(sl=True, type="transform")
    for obj in sel:
        rig.group_freeze(obj)


def insert_group_above(*args):
    sel = cmds.ls(sl=True)

    for obj in sel:
        par = cmds.listRelatives(obj, p=True)

        grp = cmds.group(em=True, n="{}_Grp".format(obj))

        pos = cmds.xform(obj, q=True, ws=True, rp=True)
        rot = cmds.xform(obj, q=True, ws=True, ro=True)

        cmds.xform(grp, ws=True, t=pos)
        cmds.xform(grp, ws=True, ro=rot)

        cmds.parent(obj, grp)
        if par:
            cmds.parent(grp, par[0])


def freeze_and_connect(*args):
    #---------------- recreate hierarchy
    sel = cmds.ls(sl=True)

    ctrlOrig = sel[0]

    for x in range(1, len(sel)):
        obj = sel[x]
        ctrl = cmds.duplicate(ctrlOrig, n="{}Ctrl".format(obj))[0]

        pos = cmds.xform(obj, ws=True, q=True, rp=True)
        rot = cmds.xform(obj, ws=True, q=True, ro=True)

        grp = cmds.group(em=True, n="{}Grp".format(ctrl))

        cmds.parent(ctrl, grp)
        cmds.xform(grp, ws=True, t=pos)
        cmds.xform(grp, ws=True, ro=rot)

        cmds.parentConstraint(ctrl, obj)


def parent_chain(*args):
    # parent chain (select objs, child first. WIll parent in order selected)

    sel = cmds.ls(sl=True)
    sizeSel = len(sel)
    for x in range(0, sizeSel - 1):
        cmds.parent(sel[x], sel[x + 1])


def select_hi(*args):
    cmds.select(hi=True)


def select_components(*args):
    sel = cmds.ls(sl=True)
    if sel:
        for obj in sel:
            shape = cmds.listRelatives(obj, s=True)[0]

            if cmds.objectType(shape) == "nurbsCurve":
                cmds.select(cmds.ls("{}.cv[*]".format(obj), fl=True))
            elif cmds.objectType(shape) == "mesh":
                cmds.select(cmds.ls("{}.vtx[*]".format(obj), fl=True))
            else:
                return


def hammer_skin_weights(*args):
    mel.eval("weightHammerVerts")


def create_locator(*args):
    cmds.spaceLocator()


def changeColor(color, *args):
    """change shape color of selected objs"""

    sel = cmds.ls(sl=True)

    if sel:
        for obj in sel:
            shapes = cmds.listRelatives(obj, s=True)
            if shapes:
                for shape in shapes:
                    cmds.setAttr("%s.overrideEnabled" % shape, 1)
                    cmds.setAttr("%s.overrideColor" % shape, color)


def copy_skinning(*args):
    """select the orig bound mesh, then the new unbound target mesh and run"""

    sel = cmds.ls(sl=True)
    orig = sel[0]
    target = sel[1]

    # get orig obj joints
    try:
        jnts = cmds.skinCluster(orig, q=True, influence=True)
    except:
        cmds.warning("couldn't get skin weights from {}".format(orig))

    # bind the target with the jnts
    try:
        targetClus = cmds.skinCluster(jnts, target, bindMethod=0, skinMethod=0,
                                      normalizeWeights=1, maximumInfluences=3,
                                      obeyMaxInfluences=False, tsb=True)[0]
        print targetClus
    except:
        cmds.warning("couln't bind to {}".format(target))

    # get skin clusters
    origClus = mel.eval("findRelatedSkinCluster " + orig)

    # copy skin weights from orig to target
    try:
        cmds.copySkinWeights(ss=origClus, ds=targetClus, noMirror=True,
                             sa="closestPoint", ia="closestJoint")
    except:
        cmds.warning(
            "couldn't copy skin weights from {0} to {1}".format(orig, target))


def center_joint(*args):
    """creates a center loc on the avg position"""

# TODO -------- differentiate if these are objs or points
    sel = cmds.ls(sl=True, fl=True)
    if sel:
        ps = []
        for vtx in sel:
            ps.append(cmds.pointPosition(vtx))

        # this is cool!
        center = rig.average_vectors(ps)
        cmds.select(cl=True)
        jnt = cmds.joint(name="center_JNT")
        cmds.xform(jnt, ws=True, t=center)


def hide_shape(*args):
    """toggels the vis of the shape nodes of the selected objects"""

    sel = cmds.ls(sl=True)
    if sel:
        for obj in sel:
            shp = cmds.listRelatives(obj, shapes=True)
            if shp:
                for s in shp:
                    if cmds.getAttr("{}.visibility".format(s)):
                        cmds.setAttr("{}.visibility".format(s), 0)
                    else:
                        cmds.setAttr("{}.visibility".format(s), 1)


def bBox(*args):
    """creates a control based on the bounding box"""
    sel = cmds.ls(sl=True, type="transform")
    if sel:
        rig.bounding_box_ctrl(sel)


##########
# load function
##########

def tools(*args):
    tools_UI()
