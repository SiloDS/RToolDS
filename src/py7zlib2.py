#!/usr/bin/python -u
#
# Python Bindings for LZMA
#
# Copyright (c) 2004-2006 by Joachim Bauch, mail@joachim-bauch.de
# 7-Zip Copyright (C) 1999-2005 Igor Pavlov
# LZMA SDK Copyright (C) 1999-2005 Igor Pavlov
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# $Id: py7zlib.py 115 2006-06-18 10:53:56Z jojo $
#
"""Read from and write to 7zip format archives.
"""

#@PydevCodeAnalysisIgnore

from cStringIO import StringIO
from struct import pack, unpack
from zlib import crc32
import pylzma

MAGIC_7Z = '7z\xbc\xaf\x27\x1c'

PROPERTY_END = '\x00'
PROPERTY_HEADER = '\x01'
PROPERTY_ARCHIVE_PROPERTIES = '\x02'
PROPERTY_ADDITIONAL_STREAMS_INFO = '\x03'
PROPERTY_MAIN_STREAMS_INFO = '\x04'
PROPERTY_FILES_INFO = '\x05'
PROPERTY_PACK_INFO = '\x06'
PROPERTY_UNPACK_INFO = '\x07'
PROPERTY_SUBSTREAMS_INFO = '\x08'
PROPERTY_SIZE = '\x09'
PROPERTY_CRC = '\x0a'
PROPERTY_FOLDER = '\x0b'
PROPERTY_CODERS_UNPACK_SIZE = '\x0c'
PROPERTY_NUM_UNPACK_STREAM = '\x0d'
PROPERTY_EMPTY_STREAM = '\x0e'
PROPERTY_EMPTY_FILE = '\x0f'
PROPERTY_ANTI = '\x10'
PROPERTY_NAME = '\x11'
PROPERTY_CREATION_TIME = '\x12'
PROPERTY_LAST_ACCESS_TIME = '\x13'
PROPERTY_LAST_WRITE_TIME = '\x14'
PROPERTY_ATTRIBUTES = '\x15'
PROPERTY_COMMENT = '\x16'
PROPERTY_ENCODED_HEADER = '\x17'

class FormatError( Exception ):
    pass

class Base: #IGNORE:W0232
    """ base class with support for various basic read/write functions """
    
    def _readReal64Bit( self, file ): #IGNORE:W0622
        res = file.read( 8 )
        a, b = unpack( '<LL', res )
        return b << 32 | a, res
    
    def _read64Bit( self, file ): #IGNORE:W0622
        b = ord( file.read( 1 ) )
        mask = 0x80
        for i in xrange( 8 ):
            if b & mask == 0:
                bytes = list( unpack( '%dB' % i, file.read( i ) ) )
                bytes.reverse()
                value = ( bytes and reduce( lambda x, y: long( x ) << 8 | y, bytes ) ) or 0L
                highpart = b & ( mask - 1 )
                return value + ( long( highpart ) << ( i * 8 ) )
            
            mask >>= 1

    def _readBoolean( self, file, count, checkall = 0 ): #IGNORE:W0622
        if checkall:
            alldefined = file.read( 1 )
            if alldefined != '\x00':
                return [True] * count
            
        result = []
        b = 0
        mask = 0
        for i in xrange( count ): #IGNORE:W0612
            if mask == 0:
                b = ord( file.read( 1 ) )
                mask = 0x80
            result.append( b & mask != 0 )
            mask >>= 1
        
        return result
        

class PackInfo( Base ):
    """ informations about packed streams """
    
    def __init__( self, file ): #IGNORE:W0622
        self.packpos = self._read64Bit( file )
        self.numstreams = self._read64Bit( file )
        id = file.read( 1 ) #IGNORE:W0622
        if id == PROPERTY_SIZE:
            self.packsizes = [self._read64Bit( file ) for x in xrange( self.numstreams )] #IGNORE:W0612
            id = file.read( 1 )
            
            if id == PROPERTY_CRC:
                self.crcs = [self._read64Bit( file ) for x in xrange( self.numstreams )]
                id = file.read( 1 )
            
        if id != PROPERTY_END:
            raise FormatError, 'end id expected but %s found' % repr( id )

class Folder( Base ):
    """ a "Folder" represents a stream of compressed data """
    
    def __init__( self, file ): #IGNORE:W0622
        numcoders = self._read64Bit( file )
        self.coders = []
        self.digestdefined = False
        totalin = 0
        self.totalout = 0
        for i in xrange( numcoders ):
            while True:
                b = ord( file.read( 1 ) )
                methodsize = b & 0xf
                issimple = b & 0x10 == 0
                noattributes = b & 0x20 == 0 #IGNORE:W0612
                last_alternative = b & 0x80 == 0
                c = {}
                c['method'] = file.read( methodsize )
                if not issimple:
                    c['numinstreams'] = self._read64Bit( file )
                    c['numoutstreams'] = self._read64Bit( file )
                else:
                    c['numinstreams'] = 1
                    c['numoutstreams'] = 1
                totalin += c['numinstreams']
                self.totalout += c['numoutstreams']
                if c['method'][0] != '\x00':
                    c['properties'] = file.read( self._read64Bit( file ) )
                self.coders.append( c )
                if last_alternative:
                    break
        
        numbindpairs = self.totalout - 1
        self.bindpairs = []
        for i in xrange( numbindpairs ):
            self.bindpairs.append( ( self._read64Bit( file ), self._read64Bit( file ), ) )
        
        numpackedstreams = totalin - numbindpairs
        self.packed_indexes = []
        if numpackedstreams == 1:
            for i in xrange( totalin ):
                if self.findInBindPair( i ) < 0:
                    self.packed_indexes.append( i )
        elif numpackedstreams > 1:
            for i in xrange( numpackedstreams ):
                self.packed_indexes.append( self._read64Bit( file ) )

    def getUnpackSize( self ):
        if not self.unpacksizes: #IGNORE:E1101
            return 0
            
        r = range( len( self.unpacksizes ) ) #IGNORE:E1101
        r.reverse()
        for i in r:
            if self.findOutBindPair( i ):
                return self.unpacksizes[i] #IGNORE:E1101
        
        raise 'not found' #IGNORE:W0701

    def findInBindPair( self, index ):
        for idx in xrange( len( self.bindpairs ) ):
            a, b = self.bindpairs[idx] #IGNORE:W0612
            if a == index:
                return idx
        return - 1

    def findOutBindPair( self, index ):
        for idx in xrange( len( self.bindpairs ) ):
            a, b = self.bindpairs[idx] #IGNORE:W0612
            if b == index:
                return idx
        return - 1
        
class Digests( Base ):
    """ holds a list of checksums """
    
    def __init__( self, file, count ): #IGNORE:W0622
        self.defined = self._readBoolean( file, count, checkall = 1 )
        self.crcs = [unpack( '<l', file.read( 4 ) )[0] for x in xrange( count )] #IGNORE:W0612
    
UnpackDigests = Digests

class UnpackInfo( Base ):
    """ combines multiple folders """

    def __init__( self, file ): #IGNORE:W0622
        id = file.read( 1 ) #IGNORE:W0622
        if id != PROPERTY_FOLDER:
            raise FormatError, 'folder id expected but %s found' % repr( id )
        self.numfolders = self._read64Bit( file )
        self.folders = []
        external = file.read( 1 )
        if external == '\x00':
            self.folders = [Folder( file ) for x in xrange( self.numfolders )] #IGNORE:W0612
        elif external == '\x01':
            self.datastreamidx = self._read64Bit( file )
        else:
            raise FormatError, '0x00 or 0x01 expected but %s found' % repr( external )
        
        id = file.read( 1 )
        if id != PROPERTY_CODERS_UNPACK_SIZE:
            raise FormatError, 'coders unpack size id expected but %s found' % repr( id )
        
        for folder in self.folders:
            folder.unpacksizes = [self._read64Bit( file ) for x in xrange( folder.totalout )]
            
        id = file.read( 1 )
        if id == PROPERTY_CRC:
            digests = UnpackDigests( file, self.numfolders )
            for idx in xrange( self.numfolders ):
                folder = self.folders[idx]
                folder.digestdefined = digests.defined[idx]
                folder.crc = digests.crcs[idx]
                
            id = file.read( 1 )
        
        if id != PROPERTY_END:
            raise FormatError, 'end id expected but %s found' % repr( id )
            
class SubstreamsInfo( Base ):
    """ defines the substreams of a folder """
    
    def __init__( self, file, numfolders, folders ): #IGNORE:W0622
        self.digests = []
        self.digestsdefined = []
        id = file.read( 1 ) #IGNORE:W0622
        if id == PROPERTY_NUM_UNPACK_STREAM:
            self.numunpackstreams = [self._read64Bit( file ) for x in xrange( numfolders )] #IGNORE:W0612
            id = file.read( 1 )
        else:        
            self.numunpackstreams = []
            for idx in xrange( numfolders ): #IGNORE:W0612
                self.numunpackstreams.append( 1 )
        
        if id == PROPERTY_SIZE:
            sum = 0 #IGNORE:W0622
            self.unpacksizes = []
            for i in xrange( len( self.numunpackstreams ) ):
                for j in xrange( 1, self.numunpackstreams[i] ): #IGNORE:W0612
                    size = self._read64Bit( file )
                    self.unpacksizes.append( size )
                    sum += size
                self.unpacksizes.append( folders[i].getUnpackSize() - sum )
                
            id = file.read( 1 )

        if id == PROPERTY_CRC:
            numdigests = 0
            numdigeststotal = 0
            for i in xrange( numfolders ):
                numsubstreams = self.numunpackstreams[i]
                if numsubstreams != 1 or not folders[i].digestdefined:
                    numdigests += numsubstreams
                numdigeststotal += numsubstreams
            
            digests = Digests( file, numdigests )
            didx = 0
            for i in xrange( numfolders ):
                folder = folders[i]
                numsubstreams = self.numunpackstreams[i]
                if numsubstreams == 1 and folder.digestdefined:
                    self.digestsdefined.append( True )
                    self.digests.append( folder.crc )
                else:
                    for j in xrange( numsubstreams ):
                        self.digestsdefined.append( digests.defined[didx] )
                        self.digests.append( digests.crcs[didx] )
                        didx += 1
                            
            id = file.read( 1 )
            
        if id != PROPERTY_END:
            raise FormatError, 'end id expected but %s found' % repr( id )

        if not self.digestsdefined:
            self.digestsdefined = [False] * numdigeststotal
            self.digests = [0] * numdigeststotal

class StreamsInfo( Base ):
    """ informations about compressed streams """
    
    def __init__( self, file ): #IGNORE:W0622
        id = file.read( 1 ) #IGNORE:W0622
        if id == PROPERTY_PACK_INFO:
            self.packinfo = PackInfo( file )
            id = file.read( 1 )
        
        if id == PROPERTY_UNPACK_INFO:
            self.unpackinfo = UnpackInfo( file )
            id = file.read( 1 )
            
        if id == PROPERTY_SUBSTREAMS_INFO:
            self.substreamsinfo = SubstreamsInfo( file, self.unpackinfo.numfolders, self.unpackinfo.folders )
            id = file.read( 1 )
        
        if id != PROPERTY_END:
            raise FormatError, 'end id expected but %s found' % repr( id )

class FilesInfo( Base ):
    """ holds file properties """
    
    def _readTimes( self, file, files, name ): #IGNORE:W0622
        defined = self._readBoolean( file, len( files ), checkall = 1 )
        
        for i in xrange( len( files ) ):
            if defined[i]:
                files[i][name] = self._readReal64Bit( file )[0] #unpack('<L', file.read(4))[0]
            else:
                files[i][name] = None

    def __init__( self, file ): #IGNORE:W0622
        self.numfiles = self._read64Bit( file )
        self.files = [{'emptystream': False} for x in xrange( self.numfiles )]
        numemptystreams = 0
        while True:
            typ = self._read64Bit( file )
            if typ > 255:
                raise FormatError, 'invalid type, must be below 256, is %d' % typ
                
            typ = chr( typ )
            if typ == PROPERTY_END:
                break
                
            size = self._read64Bit( file )
            buffer = StringIO( file.read( size ) ) #IGNORE:W0622
            if typ == PROPERTY_EMPTY_STREAM:
                isempty = self._readBoolean( buffer, self.numfiles )
                map( lambda x, y: x.update( {'emptystream': y} ), self.files, isempty )  #IGNORE:W0141
                for x in isempty:
                    if x: numemptystreams += 1
                emptyfiles = [False] * numemptystreams #IGNORE:W0612
                antifiles = [False] * numemptystreams #IGNORE:W0612
            elif typ == PROPERTY_EMPTY_FILE:
                emptyfiles = self._readBoolean( buffer, numemptystreams )
            elif typ == PROPERTY_ANTI:
                antifiles = self._readBoolean( buffer, numemptystreams )
            elif typ == PROPERTY_NAME:
                external = buffer.read( 1 )
                if external != '\x00':
                    self.dataindex = self._read64Bit( buffer )
                    raise NotImplementedError
                    
                for f in self.files: #IGNORE:W0621
                    name = ''
                    while True:
                        ch = buffer.read( 2 )
                        if ch == '\0\0':
                            f['filename'] = unicode( name, 'utf-16' )
                            break
                        name += ch
            elif typ == PROPERTY_CREATION_TIME:
                self._readTimes( buffer, self.files, 'creationtime' )
            elif typ == PROPERTY_LAST_ACCESS_TIME:
                self._readTimes( buffer, self.files, 'lastaccesstime' )
            elif typ == PROPERTY_LAST_WRITE_TIME:
                self._readTimes( buffer, self.files, 'lastwritetime' )
            elif typ == PROPERTY_ATTRIBUTES:
                defined = self._readBoolean( buffer, self.numfiles, checkall = 1 )
                for i in xrange( self.numfiles ):
                    f = self.files[i]
                    if defined[i]:
                        f['attributes'] = unpack( '<L', buffer.read( 4 ) )[0]
                    else:
                        f['attributes'] = None
            else:
                raise FormatError, 'invalid type %s' % repr( typ )
        
class Header( Base ):
    """ the archive header """
    
    def __init__( self, file ): #IGNORE:W0622
        id = file.read( 1 ) #IGNORE:W0622
        if id == PROPERTY_ARCHIVE_PROPERTIES:
            self.properties = ArchiveProperties( file )
            id = file.read( 1 )
        
        if id == PROPERTY_ADDITIONAL_STREAMS_INFO:
            self.additional_streams = StreamsInfo( file )
            id = file.read( 1 )
        
        if id == PROPERTY_MAIN_STREAMS_INFO:
            self.main_streams = StreamsInfo( file )
            id = file.read( 1 )
            
        if id == PROPERTY_FILES_INFO:
            self.files = FilesInfo( file )
            id = file.read( 1 )
            
        if id != PROPERTY_END:
            raise FormatError, 'end id expected but %s found' % ( repr( id ) )

class ArchiveFile:
    """ wrapper around a file in the archive """
    
    def __init__( self, info, start, src_start, size, folder, archive, maxsize = None ):
        self.digest = None
        self._archive = archive
        self._file = archive._file #IGNORE:W0212
        self._start = start
        self._src_start = src_start
        self._folder = folder
        self.size = size
        # maxsize is only valid for solid archives
        self._maxsize = maxsize
        for k, v in info.items():
            setattr( self, k, v )
        self.reset()

    def reset( self ):
        self.pos = 0 #IGNORE:W0201
    
    def read( self ):
        data = ''
        idx = 0 #IGNORE:W0612
        cnt = 0 #IGNORE:W0612
        dec = pylzma.decompressobj( maxlength = self._start + self.size )
        self._file.seek( self._src_start )
        dec.decompress( self._folder.coders[0]['properties'] )
        total = self.compressed #IGNORE:E1101
        if total is None:
            remaining = self._start + self.size
            out = StringIO()
            while remaining > 0:
                data = self._file.read( 1024 )
                tmp = dec.decompress( data, remaining )
                out.write( tmp )
                remaining -= len( tmp )
            
            data = out.getvalue()
        else:
            data = dec.decompress( self._file.read( total ), self._start + self.size )
        return data[self._start:self._start + self.size]

    def read_size( self, toread ):
        data = ''
        idx = 0 #IGNORE:W0612
        cnt = 0 #IGNORE:W0612
        dec = pylzma.decompressobj( maxlength = self._start + toread )
        self._file.seek( self._src_start )
        dec.decompress( self._folder.coders[0]['properties'] )
        total = self.compressed #IGNORE:E1101
        if total is None:
            remaining = self._start + toread
            out = StringIO()
            while remaining > 0:
                data = self._file.read( 1024 )
                tmp = dec.decompress( data, remaining )
                out.write( tmp )
                remaining -= len( tmp )
            
            data = out.getvalue()
        else:
            data = dec.decompress( self._file.read( total ), self._start + toread )
        return data[self._start:self._start + toread]
        
    def checkcrc( self ):
        if self.digest is None:
            return True
            
        self.reset()
        data = self.read()
        crc = crc32( data )
        # make crc unsigned
        crc = unpack( '<l', pack( '<L', crc ) )[0]
        return crc == self.digest

class Archive7z( Base ):
    """ the archive itself """
    
    def __init__( self, file ): #IGNORE:W0622
        self._file = file
        self.header = file.read( len( MAGIC_7Z ) )
        if self.header != MAGIC_7Z:
            raise FormatError, 'not a 7z file'
        self.version = unpack( 'BB', file.read( 2 ) )

        self.startheadercrc = unpack( '<l', file.read( 4 ) )[0]
        self.nextheaderofs, data = self._readReal64Bit( file )
        crc = crc32( data )
        self.nextheadersize, data = self._readReal64Bit( file )
        crc = crc32( data, crc )
        data = file.read( 4 )
        self.nextheadercrc = unpack( '<l', data )[0]
        crc = crc32( data, crc )
        if crc != self.startheadercrc:
            raise FormatError, 'invalid header data'
        self.afterheader = file.tell()
        
        file.seek( self.nextheaderofs, 1 )
        buffer = StringIO( file.read( self.nextheadersize ) ) #IGNORE:W0622
        if crc32( buffer.getvalue() ) != self.nextheadercrc:
            raise FormatError, 'invalid header data'
        
        while True:
            id = buffer.read( 1 ) #IGNORE:W0622
            if id == PROPERTY_HEADER:
                break
                
            if id != PROPERTY_ENCODED_HEADER:
                raise 'Unknown field:', repr( id ) #IGNORE:W0701
            
            streams = StreamsInfo( buffer )
            file.seek( self.afterheader + 0 )
            data = ''
            idx = 0
            for folder in streams.unpackinfo.folders:
                file.seek( streams.packinfo.packpos, 1 )
                props = folder.coders[0]['properties']
                for idx in xrange( len( streams.packinfo.packsizes ) ):
                    tmp = file.read( streams.packinfo.packsizes[idx] )
                    data += pylzma.decompress( props + tmp, maxlength = folder.unpacksizes[idx] )
                
                if folder.digestdefined:
                    if folder.crc != crc32( data ):
                        raise FormatError, 'invalid block data'
                        
            buffer = StringIO( data )
        
        self.header = Header( buffer )
        self.files = []
        
        files = self.header.files
        folders = self.header.main_streams.unpackinfo.folders
        packinfo = self.header.main_streams.packinfo
        subinfo = self.header.main_streams.substreamsinfo
        packsizes = packinfo.packsizes
        self.solid = packinfo.numstreams == 1
        if self.solid:
            # the files are stored in substreams
            if hasattr( subinfo, 'unpacksizes' ):
                unpacksizes = subinfo.unpacksizes
            else:
                unpacksizes = [x.unpacksizes[0] for x in folders]
        else:
            # every file has it's own folder with compressed data
            unpacksizes = [x.unpacksizes[0] for x in folders]
        
        fidx = 0
        obidx = 0
        src_pos = self.afterheader
        pos = 0
        maxsize = ( self.solid and packinfo.packsizes[0] ) or None
        for idx in xrange( files.numfiles ):
            info = files.files[idx]
            folder = folders[fidx]
            if not info['emptystream']:
                info['compressed'] = ( not self.solid and packsizes[obidx] ) or None
                info['uncompressed'] = unpacksizes[obidx]
                file = ArchiveFile( info, pos, src_pos, unpacksizes[obidx], folder, self, maxsize = maxsize )
                if subinfo.digestsdefined[obidx]:
                    file.digest = subinfo.digests[obidx]
                self.files.append( file )
                if self.solid:
                    pos += unpacksizes[obidx]
                else:
                    src_pos += packsizes[obidx]
                obidx += 1

                if not self.solid:
                    fidx += 1
            
        self.numfiles = len( self.files )
        self.filenames = map( lambda x: x.filename, self.files ) #IGNORE:W0141
        
    # interface like TarFile
        
    def getmember( self, name ):
        for f in self.files: #IGNORE:W0621
            if f.filename == name:
                return f
                
        return None
        
    def getmembers( self ):
        return self.files
        
    def getnames( self ):
        return self.filenames

    def list( self, verbose = True ):
        print 'total %d files in %sarchive' % ( self.numfiles, ( self.solid and 'solid ' ) or '' )
        if not verbose:
            print '\n'.join( self.filenames )
            return
            
        for f in self.files: #IGNORE:W0621
            extra = ( f.compressed and '%10d ' % ( f.compressed ) ) or ' '
            print '%10d%s%s %s' % ( f.size, extra, hex( f.digest )[2: - 1], f.filename )
            
if __name__ == '__main__':
    f = Archive7z( open( 'test.7z', 'rb' ) )
    #f = Archive7z(open('pylzma.7z', 'rb'))
    f.list()
