#!/usr/bin/env python

import argparse
import os
import zipfile
import shutil

_mineCraftBinPath = os.path.expanduser( "~/Library/Application Support/minecraft/bin" )
_mineCraftJarPath = "%s/minecraft.jar" % _mineCraftBinPath


def backupMod( modName='original') :
	'''Make a copy of active mod with the given modName'''
	modPath = "%s/minecraft-%s.jar" % ( _mineCraftBinPath, modName )
	if not os.path.exists( modPath ) :
		print( "Need to backup %s in %s " % ( modName, modPath ))
		if not os.path.exists( _mineCraftJarPath ) :
			raise RuntimeError( "Couldn't find %s" % _mineCraftJarPath )
		if os.path.islink( _mineCraftJarPath ) :
			print( "%s is a symbolic link to %s, assuming the backup is fine" % ( _mineCraftJarPath, os.readlink( _mineCraftJarPath )) )
		else :
			if os.path.isdir( _mineCraftJarPath ) :
				shutil.copytree( _mineCraftJarPath, modPath )
			else :
				shutil.copyfile( _mineCraftJarPath, modPath)
			
def activateMod( modName='original') :
	'''Make the given mod active'''
	print( "Activating mod %s", modName )
	modPath = "%s/minecraft-%s.jar" % ( _mineCraftBinPath, modName )
	if not os.path.exists( modPath ) :
		raise RuntimeError( "Can't find an installed mod with this name %s", modName)
	if not os.path.islink( _mineCraftJarPath ) : # Not a link, better to make a backup of whatever it is
		bkup = "%s.bkup" % _mineCraftJarPath
		print("Making a backup of %s as %s" % ( _mineCraftJarPath, bkup))
		os.rename( _mineCraftJarPath, bkup)
	else :
		# Remove the symbolic link
		os.unlink( _mineCraftJarPath )
	# Build a link to the active mode
	os.symlink( modPath, _mineCraftJarPath )
	print( "%s activated" % modPath)

def installMod( modName, downloaded ) :
	'''Install the given downloaded mod with the given name'''
	modPath = "%s/minecraft-%s.jar" % ( _mineCraftBinPath, modName )
	print( "Installing mod into %s" % modPath )
	if not os.path.exists( downloaded ) :
		raise RuntimeError( "Can't find %s" % downloaded )
	if os.path.exists( modPath ) :
		raise RuntimeError( "There is already an installed mod with this name %s" % modPath )
	orijar = "%s/minecraft-%s.jar" % ( _mineCraftBinPath, 'original' )
	if not os.path.exists( orijar ) :
		print "Couldn't find a copy of the original minecraft, making one"
		backupMod( 'original')
	# Make a copy of the original minecraft to mess up with it
	if os.path.isdir( orijar ) :
		shutil.copytree( orijar, modPath )
	else :
		# If a file, we need to extract the archive to be able to tweak it
		os.mkdir( modPath )
		with zipfile.ZipFile( orijar, 'r') as z :
			z.extractall( modPath)
	# Now copy all files from the downloaded mod into our work copy
	if os.path.isdir( downloaded ) :
		for f in os.listdir( downloaded ) :
			shutil.copyfile( os.path.join( downloaded, f), os.path.join( modPath, f))
	else :
		# If a file, we need to extract the archive to be able to tweak it
		with zipfile.ZipFile( downloaded, 'r') as z :
			z.extractall( modPath)
	shutil.rmtree( os.path.join( modPath, 'META-INF' ) )
	print( "%s installed in %s" % ( modName, modPath ))
	


def main() :
	# Retrieve command line options
	parser = argparse.ArgumentParser(description='MineCraft mod manager')
	parser.add_argument( "-i", "--install", nargs=2, help="( name, path ) Use the given name to install the given downloaded mod")
	parser.add_argument( "-a", "--activate", help="Activate this installed mod")
	args = parser.parse_args()
	if args.install :
		installMod( args.install[0], args.install[1] )
	if args.activate :
		activateMod( args.activate )
	#backupMod( ) # First make sure we have a backup of original install

if __name__ == "__main__":
    main()