#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 			script to backup to physically connected backup drives
import os, sys, time
from send_email import *
from custom_utilities import runcmd

_DRIVE1_LOC = '/media/backup_1_1254'
_DRIVE2_LOC = '/media/backup_2_9791'
# _DRIVE3_LOC = '/media/backup_0_0000'

_DRIVES_LOC = [_DRIVE1_LOC, _DRIVE2_LOC ]
#_DRIVES_LOC = [_DRIVE1_LOC, _DRIVE2_LOC ]
#_DRIVES_LOC = [_DRIVE1_LOC  ]
# The two drive locations
_GIT_CURRENTWORKING_FLAGS  = ['DSDfit','custompy']
#
#
# 					These are cloned across the two drives
#
# 								MISC.
_GIT_MISC_REPOS_MASTER  = ['/home/carlos/work/Notes','/home/carlos/work/CustomPython/custompy']
_GIT_MISC_REPOS_TARGETS = ['code_git_repo/MISC/Notes','code_git_repo/MISC/custompy']
_GIT_MISC_FLAGS         = ['Notes','custompy']
#
# 								TEST
#
_GIT_TEST_REPO_MASTER = ['/home/carlos/work/LANLresearch/DSD_fit','/home/carlos/work/LANLresearch/DSD_fit']
_GIT_TEST_REPO_TARGETS = ['code_git_repo/DSDfit_code','code_git_repo/test']
#
# 								DSD-FIT
#
_GIT_DSD_FIT_REPO_MASTER  = ['/home/carlos/work/LANLresearch/DSD_fit']
# _GIT_DSD_FIT_REPO_MASTER_IGNORE_FOLDER  = ['report_latex/']
_GIT_DSD_FIT_REPO_TARGETS = ['code_git_repo/DSDfit_code_new']
_GIT_DSD_FIT_FLAGS        = ['DSDfit']
#
# 								ASYMP
#
_ASYMP_RESEARCH_folder  = '/home/carlos/work/LANLresearch/AsympPDE/'
_GIT_ASYMP_REPO_MASTER  = [ _ASYMP_RESEARCH_folder+current_repo for current_repo in 
	['fortran/SFE1var_1step2','report_01112012',
	'fortran/SFE_ASYMP_1step', 'fortran/SFE_ASYMP_Rvar',
	'fortran/LINSTAB'] ]
_GIT_ASYMP_REPO_TARGETS = ['code_git_repo/ASYMP_CODE/'+current_repo for current_repo in 
	['SFE_main','LATEX','ASYMP','ASYMP2','LINSTAB'] ]
_GIT_ASYMP_FLAGS = ['SFE_main','LATEX','ASYMP','ASYMP2','LINSTAB']
#
# 							Combined repos
#
_GIT_REPOS_MASTER  = _GIT_DSD_FIT_REPO_MASTER+_GIT_ASYMP_REPO_MASTER+_GIT_MISC_REPOS_MASTER
_GIT_REPOS_TARGETS = _GIT_DSD_FIT_REPO_TARGETS+_GIT_ASYMP_REPO_TARGETS+_GIT_MISC_REPOS_TARGETS
_GIT_REPOS_FLAGS   = _GIT_DSD_FIT_FLAGS +_GIT_ASYMP_FLAGS+_GIT_MISC_FLAGS

def mount_drives():
	os.system('sudo mount -a')

def update_remote_git(git_master_loc, git_to_update_loc):
	current_loc = os.path.realpath('./')
	os.chdir(git_to_update_loc)
	os.system('git pull {}'.format(git_master_loc))
	os.chdir(current_loc)

def get_update_date(repo_loc):
	current_loc = os.path.realpath('./')
	os.chdir(repo_loc)
	os.system('git log > templog.txt')
	fo = open('templog.txt','r')
	for line in fo:
		if ( line.find('Date:') != -1):
			date_str = line.strip().replace('Date:','')
			break 
	fo.close()
	os.system('rm templog.txt')
	os.chdir(current_loc)
	return date_str

def update_git(repo_loc,file_types_to_add,levels_to_go ):
	def propose_additions(files):
		result = os.system('ls {}'.format(files))
		files_to_add_potentially = []
		if ( result == 0):
			result = os.system('ls -1 {}  > temp_backup.txt'.format(files))
			for line in open('temp_backup.txt','r'):
				result1 = os.system('git ls-files {} --error-unmatch'.format(line.strip()))
				if (result1 != 0):
					files_to_add_potentially.append(line.strip())
		return files_to_add_potentially
		
	current_loc = os.path.realpath('./')
	os.chdir(repo_loc)
	
	#git ls-files backup.py --error-unmatch
	#print file_types_to_add
	result_files = []
	seg_length = 3
	print "*******************************************\n"
	
	for file_type_to_add in file_types_to_add:
		for level_str in [ '*/'*i for i in range(levels_to_go)]:
			result_files_new  = propose_additions(level_str+file_type_to_add)
			if ( result_files_new != []): result_files.append( 
				[level_str+file_type_to_add,  result_files_new] )
	print "\n*******************************************\n"
	if ( result_files != []):
		print "New files to commit \n "
		new_files = []
		for i, list1 in enumerate(result_files):
			print "File type = ", list1[0],'\n'
			a = list1[1]
			for files1 in [a[x:x+seg_length] for x in range(0,len(a),seg_length)]:
				print ('\t {} '*len(files1)).format(*files1)
			for file1 in files1:
				new_files.append(file1)
		#print new_files
		choice = raw_input( "\n Add to repo? (y/n)" )
		if ( choice[0].lower() == 'y'):
			for file2 in new_files:
				os.system('git add {}'.format(file2))
	else:
		print "No new files to commit \n "
	
	os.system('git commit -a' )
	os.chdir(current_loc)

def update_custom_utilies_git():
	update_git(_GIT_MISC_REPOS_MASTER[1],['*.py'],1)

def check_git_log(repo_loc,original_loc):
	date_str    = get_update_date(repo_loc)
	date_str_og = get_update_date(original_loc)
	print '\t{:15}:{:35}: Updated? :{}'.format(*[repo_loc.split('/')[-1],
		date_str,date_str==date_str_og] )

def get_connected_drives():
	mounted_drives = []
	os.system('df > temp_backup.txt')
	for line in open('temp_backup.txt','r'):
		for drive_str in _DRIVES_LOC:
			if (line.find(drive_str) != -1):
				mounted_drives.append(drive_str)
	os.system('rm temp_backup.txt')
	return mounted_drives

def git_backup_repos_targets(master_repos,target_repos):
	mount_drives()
	mounted_drives = get_connected_drives()
	print "Mounted driver = ", mounted_drives
	for drive_str in mounted_drives:
		for i in range(len(master_repos)):
			target_repo = '{}/{}'.format(*[drive_str,target_repos[i]] )
			setup_target_repo(target_repo)
			#print 'Master : [', master_repos[i], ']' #,  os.path.isdir(master_repos[i]);
			#print '	Target : [', target_repo, ']' #, os.path.isdir(target_repo)
			update_remote_git(master_repos[i],target_repo)
			#check_git_log(target_repo)

def setup_target_repo(target_repo):
	if (  os.path.exists(target_repo) == False):
		os.makedirs( target_repo )
	current_loc = os.path.realpath('./')
	if ( os.system('git ls-remote {} > temp.txt'.format(target_repo)) != 0 ):
		os.chdir(target_repo)
		os.system('git init-db')
	os.chdir(current_loc)

def git_backup_DSDfit_project(flags):
	git_backup_repos_targets(_GIT_DSD_FIT_REPO_MASTER,_GIT_DSD_FIT_REPO_TARGETS)

def git_backup_ASYMP_project(flags):
	git_backup_repos_targets(_GIT_ASYMP_REPO_MASTER,_GIT_ASYMP_REPO_TARGETS)

def git_backup_all_project(flags):
	git_backup_repos_targets(_GIT_REPOS_MASTER,_GIT_REPOS_TARGETS )

def git_backup_misc_project(flags):
	git_backup_repos_targets(_GIT_MISC_REPOS_MASTER ,_GIT_MISC_REPOS_TARGETS )

def git_backup_test_project(flags):
	git_backup_repos_targets(_GIT_TEST_REPO_MASTER, _GIT_TEST_REPO_TARGETS )

def check_all_gits(flags):
	target_repos   = _GIT_REPOS_TARGETS
	original_repos = _GIT_REPOS_MASTER
	mounted_drives = get_connected_drives()
	for drive in mounted_drives:
		print '\n {} \n'.format(drive.split('/')[-1]);
		for i,repo in enumerate(target_repos):
			check_git_log('{}/{}'.format(*[drive,repo]),original_repos[i])

def update_git_choice(sys_flags):
	print sys_flags
	for i,flag in enumerate(sys_flags):
		if ( flag == '-git'):
			target_repo_str = sys_flags[i+1]
			break
	print "Target repo to commit :", target_repo_str
	for i,flag in enumerate(_GIT_REPOS_FLAGS):
		if ( target_repo_str == flag ):
			#print "flag=", flag, i
			files_to_add = ['*.f90','*.f','*.tex','*.eps','*.py','*.md','*.sh']
			# ommit_folders = ['report_latex/']
			levels_to_go = int(raw_input('How many levels (note that = 2 => */*/*.ext):'))
			print _GIT_REPOS_MASTER[i],files_to_add,levels_to_go
			update_git(_GIT_REPOS_MASTER[i],files_to_add,levels_to_go )

def update_bin(flags):
	os.system('cp /home/carlos/CustomPython/custompy/backup.py  \
		/home/carlos/CustomPython/custompy/backup_code')
	fo = open('temp.txt','w')
	fo.write('#{0} \n \t print "Date bin update: {0}"'.format(time.strftime("%m%d%Y_%H-%M")))
	fo.close()
	os.system('cat temp.txt >> backup_code')
	os.system('rm temp.txt')
	# print 'pass'

def selfemailall(flags):
	# print flags
	flag = flags[1]
	current_loc = os.path.realpath('./')
	for i, flag_target in enumerate(_GIT_REPOS_FLAGS):
		if ( flag == flag_target):
			itarget = i
			break
	# print i, _GIT_REPOS_MASTER[i]
	os.chdir(  _GIT_REPOS_MASTER[itarget] )
	os.system('git ls-files > tempchangedfile.txt')
	name_of_file= flag+'_all_file'

	print "Current working directory : " , os.path.realpath('./')
	tarfile = name_of_file+'_'+time.strftime("%m%d%Y_%H-%M")+'.tar'
	print "	Creating Tarfile : ", tarfile
	os.system('tar -cvf "{}" {}'.format(*[tarfile,'tempchangedfile.txt']))
	for i,file1 in enumerate( open('tempchangedfile.txt','r') ):
		if ( os.path.exists(file1.strip()) == True):
			os.system('tar --append --file={} {}'.format(*[tarfile,file1.strip()]) )
			print "Added ", file1.strip(), "Modification time:",\
				time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.localtime(os.path.getmtime(file1.strip())))
		else:
			print "Not a file"
	print "	Created Tarfile : ", tarfile
	print "	Compressing tar file and cleaning up"

	os.system('gzip {}'.format(tarfile) )
	# stop_here
	yesno = raw_input('Proceed to email? (y/n): ')
	# if ( yesno == 'y'): send_email_file(tarfile,os.path.realpath(tarfile+'.gz'))
	# stop_here
	text_str = get_last_commit_message()
	if ( yesno == 'y'):
		send_email(["chiquete@lanl.gov"], tarfile+'.gz', 
		text_str,sender='chiquete@lanl.gov',
		files=[os.path.realpath(tarfile+'.gz')])
	os.system('rm {}.gz'.format(tarfile) )

	os.chdir(current_loc)

def selfemailchanges(flags):
	# print flags
	flag = flags[1]
	current_loc = os.path.realpath('./')
	for i, flag_target in enumerate(_GIT_REPOS_FLAGS):
		if ( flag == flag_target):
			itarget = i
			break
	# print i, _GIT_REPOS_MASTER[i]	
	os.chdir(  _GIT_REPOS_MASTER[itarget] )
	os.system('git show --pretty="format:" --name-only master > tempchangedfile.txt')
	name_of_file= flag+'_changes_file'
	print "Current working directory : " , os.path.realpath('./')
	tarfile = name_of_file+'_'+time.strftime("%m%d%Y_%H-%M")+'.tar'
	print "Creating tarfile : ", tarfile
	os.system('tar -cvf "{}" {}'.format(*[tarfile,'tempchangedfile.txt']))

	text_str = get_last_commit_message()
	# print text_str
	text_str = text_str + '\nChanged or added files\n'
	fopen = open('tempchangedfile.txt','r')
	for line in fopen:
		text_str = text_str + '\t'+line
	# print text_str

	# stop_here
	for i,file1 in enumerate( open('tempchangedfile.txt','r') ):
		if ( os.path.exists(file1.strip()) == True):
			os.system('tar --append --file={} {}'.format(*[tarfile,file1.strip()]) )
			print "Added ", file1.strip(), "Modification time:",\
				time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.localtime(os.path.getmtime(file1.strip())))
		else:
			print "Not a file"
	print "	Created Tarfile : ", tarfile
	print "	Compressing tar file and cleaning up"
	os.system('gzip {}'.format(tarfile) )

	# yesno = ''
	# while (yesno !='y' and yesno != 'n'):
	yesno = raw_input('\nProceed to email? (y/n): ')

	# if ( yesno == 'y'): send_email_file(tarfile,os.path.realpath(tarfile+'.gz'))
	# text_str = os.path.realpath(tarfile+'.gz')
	
	if ( yesno == 'y'):
		send_email(["chiquete@lanl.gov"], tarfile+'.gz', 
		text_str,sender='chiquete@lanl.gov',
		files=[os.path.realpath(tarfile+'.gz')])
	os.system('mv {}.gz old_tar/'.format(tarfile) )
	os.chdir(current_loc)

def get_last_commit_message():
	runcmd('git log > temp.txt')
	fopen = open('temp.txt','r')
	title_str = fopen.readline()
	print "Commit name: ", (title_str.strip() ).split()[1]
	lines = '{}\n'.format(title_str.strip())
	i = 0
	while True:
		line = fopen.readline()
		i += 1
		if ( line.find('commit')  and i >= 5 ):
			break
		lines = lines + '{}\n'.format(line.strip())
	print lines
	return lines

		
def update_git_current_working_directory(flags):
	print "Current working directory : ", _GIT_CURRENTWORKING_FLAGS
	# command = ((len(_GIT_CURRENTWORKING_FLAGS))*' -git {} ').format(  \
	# 	*_GIT_CURRENTWORKING_FLAGS )
	for flag in _GIT_CURRENTWORKING_FLAGS:
		update_git_choice( ['-git',flag] )

def send_email_file(name,namepath):
	emailcmd='thunderbird -P CC2 -compose to="chiquete@lanl.gov",subject="'+name+ \
		'",body="autosent",attachment="file://'+os.path.realpath(namepath)+'"' 
	failure = os.system(emailcmd)
	print "File path : ", namepath

if __name__ == '__main__':
	print os.path.realpath('./backup.py')
	flags = ['-all', '-DSDfit', '-asymp', '-misc', '-checkrepos',
		'-git','-updatebin','-currentworking','-emailchanges','-emailall']
	descriptions = [ 'update all repositories : '+
		('{}, '*len(_GIT_REPOS_MASTER)).format(*_GIT_REPOS_MASTER),
		'update DSDfit', 'update Asymp', 'Update misc repos including : '+
		('{}, '*len(_GIT_MISC_REPOS_MASTER)).format(*_GIT_MISC_REPOS_MASTER),
		'Check whether repos are up to date','git backup of master repo w/ form -git XXXX \n '
		+'\t\twhere XXXX in '+ ('{}, '*len(_GIT_REPOS_FLAGS)).format(*_GIT_REPOS_FLAGS)
		,'update program for /usr/local/bin',
		'current working projects : '+'\t\twhere XXXX in '+ 
			('{}, '*len(_GIT_CURRENTWORKING_FLAGS)).format(*_GIT_CURRENTWORKING_FLAGS),
			'Email myself changed files from last commit, e.g. "-emailchanges DSDfit"',
			'Email myself all files in last commit, e.g. "-emailall DSDfit"']
	functions = [ git_backup_all_project, git_backup_DSDfit_project,
		git_backup_ASYMP_project, git_backup_misc_project,
		check_all_gits, update_git_choice, update_bin, 
		update_git_current_working_directory, selfemailchanges, selfemailall ]
	
	flags_applied = sys.argv[1:]
	# print sys.argv[1:]

	if (len(sys.argv) > 1):
		for flag_var in sys.argv[1:]:
			for i,flag in enumerate(flags):
				if (flag == flag_var):
					functions[i](flags_applied)
	else:
		print "usage: ./backup.py ",("{} "*len(flags)).format(*flags)
		for i,flag in enumerate(flags):
			print '\t {}:'.format(flag),descriptions[i]
