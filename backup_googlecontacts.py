#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Free of charge, send back suggestion and improvements though.
#
# .. Reach me at lyager@gmail.com
#
# Depends: python-gdata from APT
#      or: py-gdata in 'MacPorts' if you're in OSX 

import gdata
import gdata.contacts.service;
import sys


def usage(progname):
	print "%s <username> <password>" % progname
	print ""
	print "  A small piece of software to log in and grab all your"
	print "  contacts from you GMail, and output the in XML format to stdout."
	print "  Mainly for backup purposes."
	print ""
	sys.exit(0)

if len(sys.argv) < 3:
	usage(sys.argv[0])

# Create a query to overcome limits
query = gdata.contacts.service.ContactsQuery()
query.max_results = 9999

gd_client = gdata.contacts.service.ContactsService()
gd_client.email = sys.argv[1]
gd_client.password = sys.argv[2]
gd_client.source = 'https://github.com/lyager/backup_googlecontacts'
gd_client.ProgrammaticLogin()

def PrintFeed(feed):
	for i, entry in enumerate(feed.entry):
		print '\n%s %s' % (i+1, entry.title.text)
		if entry.content:
			print '		%s' % (entry.content.text)
		# Display the primary email address for the contact.
		for email in entry.email:
			if email.primary and email.primary == 'true':
				print '		%s' % (email.address)
		# Show the contact groups that this contact is a member of.
		for group in entry.group_membership_info:
			print '		Member of group: %s' % (group.href)
		# Display extended properties.
		for extended_property in entry.extended_property:
			if extended_property.value:
				value = extended_property.value
			else:
				value = extended_property.GetXmlBlobString()
			print '		Extended Property - %s: %s' % (extended_property.name, value)


feed = gd_client.GetContactsFeed(query.ToUri())
print feed
