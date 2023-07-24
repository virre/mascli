# Mascli
 This is just a simple thing I did to be able to get the public timeline from multiple mastadon instances in one go. I decided to write it in Python because I needed a head refresh on vacation from the PHP I get paid to write. 

## Usage

This is a minimal early version, it needs a ini file in the home directory named mascli that looks like this:

       
	 [instances]
	 instances = instance.name,instance2.name
       

when that exists you can just call mascli.py, the standard display will show three toots from each instances public timeline but
		this possible to effect by adding --limit x for the number of toots per instance to show.

## TODO:
  Like everything, the only reason I am even uploading this to the Internet is that I noticed a lot of people talking about wanting
		this type of view of multiple public timelines. Things todo is like better output, possibly look into more access but also someway
		to make it possible to easily follow people etc. (Like at least intergrate so you can open links). So much stuff, also code quality I 
		am sure can up a lot, as mentioned I do not really write Python often. 
