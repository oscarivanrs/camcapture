from random import gauss
from sys import _current_frames
from threading import local
from typing import Iterable
import cv2
import numpy
from PIL import Image
import datetime
import os
from functools import reduce
import configparser
import itertools

print( "mom release = 2022.019.973" )

#Load properties
prop = configparser.ConfigParser()
prop.read( 'mom.properties' )

_decidedly_not_similar_rate = prop.getint( 'mom-param', 'not_similar_default_rate', fallback=10000000)
_text_font_scale = prop.getfloat( 'mom-param', 'text_font_scale', fallback=1.0)
_text_thickness = prop.getint( 'mom-param', 'text_thickness', fallback=1 ) 
_text_background_aplha = prop.getfloat( 'mom-param', 'text_backround_alpha', fallback=0.4 )
_text_background_color = tuple( prop.get( 'mom-param', 'text_background_color', fallback='200,200,200').split( '.' ))
_text_backgroung = prop.getboolean( 'mom-param', 'text_background', fallback=False )
_black_and_white = prop.getboolean( 'mom-param', 'black_white_text', fallback=False )
_default_text_color = tuple( int(val) for val in prop.get('mom-param', 'default_text_color', fallback='0,0,0').split( ',' ) )
_gray_scale = prop.getboolean( 'mom-param', 'gray_scale', fallback=False)
_gaussian_blur = prop.getboolean( 'mom-param', 'gaussian_blur', fallback=True )
_kernel_size = tuple( int(val) for val in tuple( prop.get( 'mom-param', 'kernel_size', fallback='7,7').split( ',' ) ))
_threshold_distance = prop.getint( 'mom-param', 'threshold_distance', fallback=60 )
_bruteforce_hamm = prop.getboolean( 'mom-param', 'hamming_bruteforce', fallback=False )
_minimum_points = prop.getint( 'mom-param', 'minimum_compare_points', fallback=32)

_permitted_extensions=set( ["jpg"] )

def set_extensions( ext: str ):
    """
        This function permits to set accetable pictures extensions. Value supplied must contains values
        separated by , character ( comma ).

        If arguments is None or equals to void string, raises a ValueError.
    """
    global _permitted_extensions
    if not str or str == '':
        raise ValueError( 'No extension supplied to mom. It uses default extensions', _permitted_extensions )
    _permitted_extensions = [ ext for ext in ext.split(',')]



def write_text_image( source: str, text: str, dest: str = None, font_scale: float = _text_font_scale, thickness: int = _text_thickness, show_result: bool = False,
                        black_and_white: _black_and_white = _black_and_white, default_color: tuple = _default_text_color, text_bkr = _text_backgroung,
                        text_bkr_alpha = _text_background_aplha, text_bkr_color = _text_background_color  ):
    """
        This function permits to add text to picture.
        If picture isn't found, function raise a ValueError.
        If text is None or a void str, function raise a ValueError.
        There will be added two line, first with black color and second with
        white color. Actually text is centered in picture.

        :param source: is path of picture where text must be added.
        :param text: is text that must be added.
        :param dest: is destination file where modified picture must be saved. If None, source file is overwrited.
        :param font_scale: is font size used to write text. Default value is stored in file mom.properties at property text_font_scale. 
        :param thickness: is the thickness of text. Default value is stored in file mom.properties at property text_thickness. Defaul value is 1
        :param show_result: is a flag that indicates if show modified picture. Default value is False. 
        :param black_and_white: is a flag that indicates if add text both white and black. Default value is stored in file mom.properties at property black_white_text. Default value is False.
        :param default_color: indicates what color must be the default color. Default value is stored in file mom.properties at property default_text_color. Default value is RGB 0,0,0
        :param text_bkr: is a flag that indicates if text must be included in a dedicated rectangle. Default value is False.
        :param text_bkr_alpha: alpha value of text background, if is expected. Valid only if text_bkr parameter is True. Default value is 0.4.
        :param text_bkr_color: color of text background. Valid only if text_bkr parameter is True. Default value is RGB 200,200,200

        Raise ValueError when source file doesn't exists, if text parameter is None or void string and if default_color parameter
        is different from black ( 0, 0, 0 ) or white( 255, 255, 255 ) RGB values.

    """
    if not os.path.exists( source ):
         raise ValueError( "source file " + source + " doesn't exists!" )
    if not text or text == '':
        raise ValueError( "No text passed to funcion!" )
    
    if default_color != ( 255,255,255 ) and default_color != ( 0, 0, 0 ):
        raise ValueError( "Wrong default_color value {}".format( default_color ) )

    if not dest:
        dest = source

   
    destination_dir = os.path.split( dest )
    if destination_dir[ 0 ] and not os.path.exists( destination_dir[ 0 ] ):
        os.makedirs( destination_dir[ 0 ] )
        

    img = Image.open( source );
    img_width, img_height = img.size
    text_size = cv2.getTextSize( text, cv2.FONT_HERSHEY_PLAIN, font_scale, thickness )
    gap = text_size[ 0 ][ 1 ] // 2

     
    second_line_y = img_height - text_size[ 0 ][ 1 ]
    first_line_y = second_line_y - text_size[ 0 ][ 1 ] - gap
    

    lines_x = ( img_width - text_size[ 0 ][ 0 ] ) // 2

    print( "destination pic = " + dest )
    print( "img size = {} ".format( img.size ) )
    print( "gap = {}".format( gap ) )  
    print( "lines x coordinate = {}".format( lines_x ) )
    print( "first line y coordinate = {}".format( first_line_y ) )              
    print( "second line y coordinate = {}".format( second_line_y ) )

    img = cv2.imread( source );
    
    if text_bkr:
        overlay = img.copy()
        rect_x = lines_x - gap;
        rect_y = first_line_y - gap if black_and_white else second_line_y
        rect_y = rect_y - text_size[ 0 ][ 1 ] - gap                                                 # coordinate of text referes to BOTTOM left corner
        rect_w = rect_x + text_size[ 0 ][ 0 ] + ( gap * 2 )
        rect_h = text_size[ 0 ][ 1 ] * 2 + ( gap * 4 ) if black_and_white else text_size[ 0 ][ 1 ] + ( gap * 2 )
        rect_h = rect_y + rect_h 
        cv2.rectangle( overlay, ( rect_x, rect_y ), ( rect_w, rect_h ), ( 200, 200, 200 ), -1  )
        alpha = text_bkr_alpha
        img = cv2.addWeighted( overlay, alpha, img, 1 - alpha, 0 )

    if black_and_white:
        cv2.putText( img, text, org=(lines_x,first_line_y), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale= font_scale, color=(255,255,255), thickness=thickness, lineType = cv2.LINE_AA )
        cv2.putText( img, text, org=(lines_x,second_line_y),fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale= font_scale, color=(0,0,0), thickness=thickness, lineType = cv2.LINE_AA )
    else:
        cv2.putText( img, text, org=(lines_x,second_line_y),fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale= font_scale, color=default_color, thickness=thickness, lineType = cv2.LINE_AA )

    cv2.imwrite( dest, img )

    if show_result:
        cv2.imshow( "Result", img )
        cv2.waitKey( 0 )
        cv2.destroyAllWindows()



def dir_best_match( pic_one: str, dir: str ) -> str:
    """
        This function permits to executes best match between one picture and others contained in a specific directory.
        Method raise a ValueError if pic_one or dir parameters are void or null, and if even one of them referes
        to a non existent file.
        Event subdirectories are considered.
        Only files with a valid extension will be considered.

        :param pic_one: path of image that must be compared with others.
        :param dir: path of directory that contains other pictures.

        Returns path of most similar picture, or string "HOPS" if no picture is similar.
    """
    if not pic_one or not os.path.exists( pic_one ):
        raise ValueError( "Error during best match on directory. pic_one parameters is None, equals to void string or \
                                    referes to file that does not exists." )

    if not dir or not os.path.exists( dir ) or not os.path.isdir( dir ):
        raise ValueError( "Error during best match on directory. dir parameters is None, equals to void string, \
                                    referes to directory that does not exists or simply is not a directory." )

    files_to_compare = _listdir( dir )

    if not files_to_compare:
        return "HOPS"
    else:
        return list_best_match( pic_one, files_to_compare )



def list_best_match( pic_one: str, others, error: int=0 ) -> str:
    """
        This function permits to executes best match between one picture and a list of others pictures.
        Only files with a valid extension will be considered. others parameter can be string or an iterable
        object.

        :param pic_one: is path of picture that must be compared to others. If None or void, function raise a ValueError.
        :param others: iterable object that contains other pictures paths. Value will be filtered in way to remove
        file with uncorrect extension. If is a string object, will splitted by ; ( semicolon ).
        :param error: define behavior of function if function don't find a picture or if one of them in list
        has wrong extension. If '0', function simply discards wrong file. Otherwise:

            -raise ValueError if extension isn't permitted.

            -raise FileNotFoundError if file isn't found.

        Returns path of most similar picture, or string "HOPS" if no similar picture is found.
    """
    if not pic_one or not os.path.exists( pic_one ) :
        raise ValueError( "Error during best match on list of files. pic_one parameters is None, equals to void string or \
                                    referes to file that does not exists." )
    
    best_match = ( None, _decidedly_not_similar_rate )
    match_map = dict()

    if isinstance( others, str ):
        others = others.split( ',' )

    for current_pic in others:
        if not os.path.exists( current_pic ):
            if error == 0:
                continue
            else:
                raise FileNotFoundError( "Picture file " + current_pic + " not found" )
        if str( current_pic ).split( "." )[ -1 ] not in _permitted_extensions:
            if error == 0:
                continue
            else:
                raise ValueError( "Pciture file " + current_pic + " has extension that isn't permitted" )
        if pic_one == current_pic:
            continue;
        current_match = orb_compare( pic_one, current_pic )
        match_map[ current_pic ] = current_match
        if current_match < best_match[ 1 ]:
            best_match = ( current_pic, current_match )
    
    print( "Match map for img ", pic_one )
    for match_img, match_value in match_map.items():
        print( "pic name = ", match_img, "match value = ", match_value )

    print( "Best match details: pic = {} rate = {}".format( best_match[ 0 ], best_match[ 1 ] ) )
    if best_match[ 1 ] == _decidedly_not_similar_rate:
        return "HOPS"
    else:
        return best_match[ 0 ]

    
def orb_compare( pic_one: str, pic_two: str, gray_scale: bool=_gray_scale, gaussian_blur: bool=_gaussian_blur, show_result: bool=False, g_kernel_size:tuple= _kernel_size,
                    max_points_distance: int= _threshold_distance, bruteforce_hamm: bool=_bruteforce_hamm ) -> float:
    """
        Executes pictures comparison based on ORB algorithm. Rate value returned is calcualted with internal 3esse algorithm that can be
        varies in future. Smaller is value, the more similar pictures are.

        :param pic_one: path of picture
        :param pic_two: path of compared picture
        :param gray_scale: flag that indicates if  pictures must be converted in gray scale. Default value is stored in file mom.properties at property gray_scale.
        :param gaussian_blur: flag that indicates if pictures must be blurred. Default value is stored in file mom.properties at property gaussian_blur.
        :param show_result: flag that indicates if result of comparison must be showed. Default value is False.
        :param g_kernel_size: tuple that contains value of kernel_size used by ORB algorithm. Default value is stored in mom.properties at property kernel_size.
        :param max_points_distance: value that indicates threshold for acceptable points.Default vale is stored in mom.properties at property trheshold_distance.
        :param bruteforce_hamm: flag that indicates if hamming brute force must be used. Default value is stored in mom.properties at property hamming_bruteforce.
    """

    error_line = "Picture defined by value of {} parameter not found"

    if not os.path.exists( pic_one ):
        raise ValueError( error_line.format( pic_one ) )

    if not os.path.exists( pic_two ):
        raise ValueError( error_line.format( pic_two ) )

    print( "Comparing {} with {} with ORB algorithm".format( pic_one, pic_two ) )
    pic_one = cv2.imread( pic_one )
    pic_two = cv2.imread( pic_two )

    if gray_scale:                                                              
        pic_one = cv2.cvtColor( pic_one, cv2.COLOR_BGR2GRAY )
        pic_two = cv2.cvtColor( pic_two, cv2.COLOR_BGR2GRAY )
    
    if gaussian_blur:                                
        pic_one = cv2.GaussianBlur( pic_one, g_kernel_size, 0 )
        pic_two = cv2.GaussianBlur( pic_two, g_kernel_size, 0 )

    orb = cv2.ORB_create()
    pic_one_points, pic_one_desc = orb.detectAndCompute( pic_one, None )            
    pic_two_points, pic_two_desc = orb.detectAndCompute( pic_two, None )

    matcher = cv2.BFMatcher( cv2.NORM_HAMMING, crossCheck=False )

    matches = matcher.match( pic_one_desc, pic_two_desc )                          

    if show_result:
        result = cv2.drawMatches( pic_one, pic_one_points, pic_two, pic_two_points, matches[:20], None )
        result = cv2.resize( result, ( 1000, 650 ) )
        cv2.imshow( "Result", result )
        cv2.waitKey( 0 )
        cv2.destroyAllWindows()
    
    return _analyze_orb_matches( matches )


def _analyze_orb_matches( matches ) -> float:
    """
        This function computes value of similarity between two picture. Returns float
        value:  the smaller the value, the more similar the photos are.
        If returned value is equals to _decidedly_not_similar_rate, can be conclused
        that picture isn't definetle not similar.

        :param matches: tuple with DMatch point retrieved by ORB algorithm
    """
    # Matches contains DMatch objects.
    # Every DMatch object has:
    # DMatch.distance - Distance between descriptors. The lower, the better it is.
    # DMatch.trainIdx - Index of the descriptor in train descriptors(1st image).
    # DMatch.queryIdx - Index of the descriptor in query descriptors(2nd image).
    # DMatch.imgIdx - Index of the train image.

    print( "Fond {} contact points ".format( len( matches )))

    filtered_matches = [ match for match in matches if match.distance < _threshold_distance ]
    print( "Found {} valid contatct points ".format( len(filtered_matches)))
    if len( filtered_matches ) < _minimum_points:
        print( "Only {} contact's points satisfy {} threshold value. Picture are decidedly not similar".format( len( filtered_matches ), _minimum_points) )
        return _decidedly_not_similar_rate

    """
        To obtain a value that can indicates similitude of pictures, we are following
        below steps:
        - matches tuple is ordered in relation of distance value of each DMatch object.
        - from ordere tuple is extraced, starting from last element, a section which size
            is equals to @minimum_points parameters values.
        - this section is splitted in quarter
        - First and last quarter are summed.
        - Proportion between values is executed
        Be aware: this algorithm was thought of by us: can be modified in future.
    """

    filtered_matches.sort( key=lambda current_p: current_p.distance, reverse=True )

    media = _minimum_points // 4

    valid_matches = filtered_matches[ -_minimum_points : ]
    first_quarter = valid_matches[ 0 : media ]
    last_quarter = valid_matches[ -media :  ]

    lambda_exp = lambda current_p : current_p.distance

    greather = sum( map( lambda_exp, valid_matches ))
    larger = sum( map( lambda_exp, first_quarter ))
    smaller = sum( map( lambda_exp, last_quarter  ))

    larger = 1 if larger == 0 else larger
    smaller = 1 if smaller == 0 else smaller

    rectified = smaller / larger
    accurance = greather * rectified
    rate = ( smaller + larger ) * rectified

    trace = "match:{}\nmaximo:{} Rettifica:{} Piccoli:{} Grandi:{} Accurance:{} Rate:{}".format( len( filtered_matches ) ,greather, rectified, smaller/ media, larger / media,accurance, rate )
    print( trace )
    return rate
    

def _listdir( directory: str ) -> list: 
    """
        Searches valid files in given directory. Function inspects even all sub directory.
        Only files with permitted extensions are taken.
        If given path isn't a directory raise a ValueError.

        :param directory: root directory where search files.
    """
    if not os.path.isdir( directory ):
        raise ValueError( "Given path is not a directory" )

    print( "Searching for valid files in {} directory".format( directory ) )
    files_list = []
    for root_dir, sub_dir, files in os.walk( directory ):
        files_list.append([ os.path.join( root_dir, file ) for file in files if file.split('.')[-1] in _permitted_extensions ])
    files_list = itertools.chain.from_iterable( files_list )
    return files_list




if __name__ == '__main__':
    text = datetime.datetime.now().strftime( "%H:%M:%S" )
    write_text_image( r"/home/stefano/Scrivania/workspaces/roungickVdf20/CAMERAcode/src/demo/catalogue/0008001120876348/WA1.jpg", text, r"/tmp/0008001120876348/WA1.jpg", black_and_white = True,show_result = True, text_bkr=True)

    #rate = orb_compare( r"/home/stefano/Scrivania/workspaces/roungickVdf20/CAMERAcode/src/demo/catalogue/0008001120876348/WA1.jpg", r"/tmp/prova/8001120859443.jpg", show_result=True )
    #print( rate )

    #rate = orb_compare( r"/home/stefano/Scrivania/workspaces/roungickVdf20/CAMERAcode/src/demo/catalogue/0008001120876348/WA1.jpg", r"/tmp/prova/8001120859443.jpg", show_result=False)
    #print( rate )

    #rate = orb_compare( r"/home/stefano/Scrivania/workspaces/roungickVdf20/CAMERAcode/src/demo/catalogue/0008001120876348/WA1.jpg", r"/tmp/prova/8001120859443.jpg", show_result=False )
    #print( rate )

    #rate = orb_compare( r"/home/stefano/Scrivania/workspaces/roungickVdf20/CAMERAcode/src/demo/catalogue/0008001120876348/WA1.jpg", r"/home/stefano/Scrivania/workspaces/roungickVdf20/CAMERAcode/src/demo/catalogue/0008001120876348/1234567890/ICCC00000010011001234567890.jpg",show_result=True  )
    #print( rate )

    #files = _listdir( r'/home/stefano/Scrivania/workspaces/roungickVdf20/CAMERAcode/src/demo' )
    #for f in files:
    #    print( f )

    #img = dir_best_match( r'/home/stefano/Scrivania/workspaces/roungickVdf20/CAMERAcode/src/demo/catalogue/0008001120876348/WA1.jpg', r'/home/stefano/Scrivania/workspaces/roungickVdf20/CAMERAcode/src/demo/catalogue/0008001120876348' )
    #print( "image = ", img )