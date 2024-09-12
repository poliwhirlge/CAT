def format_location(note_location):
    # _location_amount = len(project_time_signature_location)
    # _ppq = 480
    #
    # for _test in range(_location_amount):
    #
    #     _location_index = (_location_amount - 1) - _test
    #
    #     if note_location >= project_time_signature_location[_location_index]:
    #         _location_base = project_time_signature_location[_location_index]
    #         _location_offset = note_location - _location_base
    #
    #         _location_num = project_time_signature_location_num[_location_index]
    #         _location_denom = project_time_signature_location_denom[_location_index]
    #
    #         _divisor_factor = (_location_denom / 4)
    #         _divisor = (_ppq / _divisor_factor) * _location_num
    #
    #         _time_1 = (_location_offset / _divisor) + project_time_signature_location_measure[_location_index]
    #         _time_2 = (_location_offset % _divisor) / (_ppq / (_location_denom / 4))
    #
    #         return str(int(_time_1 + 1)) + '.' + str(int(_time_2 + 1))

    return "Error.Error"


def write_html_output(output_file_name: str, page_title: str, reaper_file_name: str, dTmpl: dict, available_tracks: set):

    with open(output_file_name, 'w', encoding='utf-8') as f:
        var_html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <HEAD>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <!-- Le styles -->
        <link href="css/bootstrap.min.css" rel="stylesheet">
        <link href='http://fonts.googleapis.com/css?family=Open+Sans:400,300,700'
     rel='stylesheet' type='text/css'>
        <style type="text/css">
            body {{
                color: #333;
                padding-bottom: 40px;
            }}
            .sidebar-nav {{
                padding: 9px 0;
            }}
        </style>
        <!--<link href="css/bootstrap-responsive.css" rel="stylesheet">        -->
        <link href="css/carv.css" rel="stylesheet">
        <title>{page_title}</title>
    </HEAD>
    <body>
        <div class="container-fluid">
            <h3 style="color: white; padding-top:16px; padding-bottom:16px;">{reaper_file_name}</h3>
            <ul class="nav nav-tabs" >'''

        if 'drums' in available_tracks:
            var_html += '''<li class="active"><a href="#tab_drums" data-toggle="tab">Drums ''' + dTmpl[
                'drums_error_icon'] + '''</a></li>'''
        if 'drums_2x' in available_tracks:
            var_html += '''<li><a href="#tab_drums_2x" data-toggle="tab">Drums (2x) ''' + dTmpl[
                'drums_2x_error_icon'] + '''</a></li>'''
        if 'bass' in available_tracks:
            var_html += '''<li><a href="#tab_bass" data-toggle="tab">Bass ''' + dTmpl['bass_error_icon'] + '''</a></li>'''
        if 'guitar' in available_tracks:
            var_html += '''<li><a href="#tab_guitar" data-toggle="tab">Guitar ''' + dTmpl[
                'guitar_error_icon'] + '''</a></li>'''
        if 'rhythm' in available_tracks:
            var_html += '''<li><a href="#tab_rhythm" data-toggle="tab">Rhythm ''' + dTmpl[
                'rhythm_error_icon'] + '''</a></li>'''
        if 'prokeys' in available_tracks:
            var_html += '''<li><a href="#tab_prokeys" data-toggle="tab">Pro Keys ''' + dTmpl[
                'prokeys_error_icon'] + '''</a></li>'''
        if 'keys' in available_tracks:
            var_html += '''<li><a href="#tab_keys" data-toggle="tab">Keys ''' + dTmpl['keys_error_icon'] + '''</a></li>'''
        if 'vocals' in available_tracks:
            var_html += '''<li><a href="#tab_vocals" data-toggle="tab">Vocals ''' + dTmpl[
                'vocals_error_icon'] + '''</a></li>'''
        if 'harm1' in available_tracks:
            var_html += '''<li><a href="#tab_harm1" data-toggle="tab">Harmony 1 ''' + dTmpl[
                'harm1_error_icon'] + '''</a></li>'''
        if 'harm2' in available_tracks:
            var_html += '''<li><a href="#tab_harm2" data-toggle="tab"> 2 ''' + dTmpl['harm2_error_icon'] + '''</a></li>'''
        if 'harm3' in available_tracks:
            var_html += '''<li><a href="#tab_harm3" data-toggle="tab"> 3 ''' + dTmpl['harm3_error_icon'] + '''</a></li>'''
        var_html += '''<li><a href="#tab_events" data-toggle="tab">Events ''' + dTmpl['events_error_icon'] + '''</a></li>'''
        var_html += '''<!--<li><a href="#tab_venue" data-toggle="tab">Venue ''' + dTmpl[
            'venue_error_icon'] + '''</a></li>-->'''
        var_html += '''<li><a href="#tab_od" data-toggle="tab">OD Graph</a></li>
            </ul>
        </div>
        <div class="container-fluid">
            <div class="row-fluid" style="background-color: white;">
                <div class="span9">
                    <div class="tabbable">
                        <div class="span2">
                            <div class="well sidebar-nav">
                                <h class="nav-list" style="font-weight: bold; font-size: 18px;">At a glance</h>
                                <ul class="nav nav-list">
                                    '''
        if 'drums' in available_tracks:
            var_html += '''<section>
            <li class="nav-header">Drums</li>
            <li class=""><a href="#">OD Count: ''' + "{}".format(dTmpl['drums_total_ods']) + '''</a></li>
            <li class=""><a href="#">Fill Count: ''' + "{}".format(dTmpl['drums_total_fills']) + '''</a></li>
            <li class=""><a href="#">Kicks on X: ''' + "{}".format(dTmpl['drums_total_kicks_x']) + '''</a></li>
            <li class=""><a href="#">Kicks on H: ''' + "{}".format(dTmpl['drums_total_kicks_h']) + '''</a></li>
            <li class=""><a href="#">Kicks on M: ''' + "{}".format(dTmpl['drums_total_kicks_m']) + '''</a></li>
            <li class=""><a href="#">Kicks on E: ''' + "{}".format(dTmpl['drums_total_kicks_e']) + '''</a></li>
            </section>
            '''
        if 'drums_2x' in available_tracks:
            var_html += '''<section>
        <li class="nav-header">Drums (2x)</li>
        <li class=""><a href="#">OD Count: ''' + "{}".format(dTmpl['drums_2x_total_ods']) + '''</a></li>
        <li class=""><a href="#">Fill Count: ''' + "{}".format(dTmpl['drums_2x_total_fills']) + '''</a></li>
        <li class=""><a href="#">Kicks on X: ''' + "{}".format(dTmpl['drums_2x_total_kicks_x']) + '''</a></li>
        <li class=""><a href="#">Kicks on H: ''' + "{}".format(dTmpl['drums_2x_total_kicks_h']) + '''</a></li>
        <li class=""><a href="#">Kicks on M: ''' + "{}".format(dTmpl['drums_2x_total_kicks_m']) + '''</a></li>
        <li class=""><a href="#">Kicks on E: ''' + "{}".format(dTmpl['drums_2x_total_kicks_e']) + '''</a></li>
        </section>
        '''
        if 'bass' in available_tracks:
            var_html += '''<section>
        <li class="nav-header">Bass</li>
        <li class=""><a href="#">OD Count: ''' + "{}".format(dTmpl['bass_total_ods']) + '''</a></li>
        </section>
        '''
        if 'guitar' in available_tracks:
            var_html += '''<section>
        <li class="nav-header">Guitar</li>
        <li class=""><a href="#">OD Count: ''' + "{}".format(dTmpl['guitar_total_ods']) + '''</a></li>
        </section>
        '''
        if 'rhythm' in available_tracks:
            var_html += '''<section>
        <li class="nav-header">Rhythm</li>
        <li class=""><a href="#">OD Count: ''' + "{}".format(dTmpl['rhythm_total_ods']) + '''</a></li>
        </section>
        '''
        if 'keys' in available_tracks:
            var_html += '''<section>
        <li class="nav-header">Keys</li>
        <li class=""><a href="#">OD Count:    ''' + "{}".format(dTmpl['keys_total_ods']) + '''</a></li>
        </section>
        '''
        if 'prokeys' in available_tracks:
            var_html += '''<section>
        <li class="nav-header">Pro Keys</li>
        <li class=""><a href="#">OD Count:    ''' + "{}".format(dTmpl['prokeys_total_ods']) + '''</a></li>
        </section>
        '''
        if 'vocals' in available_tracks:
            var_html += '''<section>
        <li class="nav-header">Vocals</li>
        <li class=""><a href="#">Vocals OD Count: ''' + str(len(dTmpl['vocals_od_start'])) + '''</a></li>'''
            if 'harm1' in available_tracks:
                var_html += '''<li class=""><a href="#">Harmony 1 OD Count: ''' + str(
                    len(dTmpl['harm1_od_start'])) + '''</a></li>'''

        if 'vocals' in available_tracks:
            var_html += '''</section>
        '''
        var_html += '''</ul>
                            </div><!--/.well -->
                        </div><!--/span-->
                        <div class="tab-content">
                            <div class="tab-pane active" id="tab_drums">
                                <div class="span12">'''
        if dTmpl['drums_kick_gem'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Easy Kick + Gem</h3>
                                        <div>''' + "{}".format(dTmpl['drums_kick_gem']) + '''</div>
                                    </div>'''
        if dTmpl['drums_kick_gem_m'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Medium Kick + Gems</h3>
                                        <div>''' + "{}".format(dTmpl['drums_kick_gem_m']) + '''</div>
                                    </div>'''
        if dTmpl['drums_not_found_lower'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Lower Difficulties</h3>
                                        <div>''' + "{}".format(dTmpl['drums_not_found_lower']) + '''</div>
                                    </div>'''
        if dTmpl['drums_tom_marker'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Tom Markers</h3>
                                        <div>''' + "{}".format(dTmpl['drums_tom_marker']) + '''</div>
                                    </div>'''
        if dTmpl['drums_fills_errors'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Drum Fills Issues</h3>
                                        <div>''' + "{}".format(dTmpl['drums_fills_errors']) + '''</div>
                                    </div>'''
        if dTmpl['drums_general_issues'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Drum General Issues</h3>
                                        <div>''' + "{}".format(dTmpl['drums_general_issues']) + '''</div>
                                    </div>'''
        var_html += '''
                                </div>
                            </div>
                            <div class="tab-pane" id="tab_drums_2x">
                                <div class="span12">'''
        if dTmpl['drums_2x_kick_gem'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Easy Kick + Gem</h3>
                                        <div>''' + "{}".format(dTmpl['drums_2x_kick_gem']) + '''</div>
                                    </div>'''
        if dTmpl['drums_2x_kick_gem_m'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Medium Kick + Gems</h3>
                                        <div>''' + "{}".format(dTmpl['drums_2x_kick_gem_m']) + '''</div>
                                    </div>'''
        if dTmpl['drums_2x_not_found_lower'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Lower Difficulties</h3>
                                        <div>''' + "{}".format(dTmpl['drums_2x_not_found_lower']) + '''</div>
                                    </div>'''
        if dTmpl['drums_2x_tom_marker'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Tom Markers</h3>
                                        <div>''' + "{}".format(dTmpl['drums_2x_tom_marker']) + '''</div>
                                    </div>'''
        if dTmpl['drums_2x_fills_errors'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Drum Fills Issues</h3>
                                        <div>''' + "{}".format(dTmpl['drums_2x_fills_errors']) + '''</div>
                                    </div>'''
        if dTmpl['drums_2x_general_issues'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Drum General Issues</h3>
                                        <div>''' + "{}".format(dTmpl['drums_2x_general_issues']) + '''</div>
                                    </div>'''
        var_html += '''
                                </div>
                            </div>
                            <div class="tab-pane" id="tab_bass">
                                <div class="span12">'''
        if dTmpl['bass_green_oranges_three'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Gem + G + O</h3>
                                        <div>''' + "{}".format(dTmpl['bass_green_oranges_three']) + '''</div>
                                    </div>'''
        if dTmpl['bass_chords_four_notes'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Four-Note Chords</h3>
                                        <div>''' + "{}".format(dTmpl['bass_chords_four_notes']) + '''</div>
                                    </div>'''
        if dTmpl['bass_chords_three_notes'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Three-Note Chords on Hard</h3>
                                        <div>''' + "{}".format(dTmpl['bass_chords_three_notes']) + '''</div>
                                    </div>'''
        if dTmpl['bass_chords_dont_exist'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Chord Difficulty Mismatch</h3>
                                        <div>''' + "{}".format(dTmpl['bass_chords_dont_exist']) + '''</div>
                                    </div>'''
        if dTmpl['bass_chords_h_green_orange'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">G+O Chords on Hard</h3>
                                        <div>''' + "{}".format(dTmpl['bass_chords_h_green_orange']) + '''</div>
                                    </div>'''
        if dTmpl['bass_chords_m_chord_combos'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">G+B / G+O / R+O Chords on Medium</h3>
                                        <div>''' + "{}".format(dTmpl['bass_chords_m_chord_combos']) + '''</div>
                                    </div>'''
        if dTmpl['bass_chords_m_hopos'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Forced HOPOs on Medium</h3>
                                        <div>''' + "{}".format(dTmpl['bass_chords_m_hopos']) + '''</div>
                                    </div>'''
        if dTmpl['bass_chords_easy'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Easy Chords</h3>
                                        <div>''' + "{}".format(dTmpl['bass_chords_easy']) + '''</div>
                                    </div>'''
        if dTmpl['bass_general_issues'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">General Errors / Warnings</h3>
                                        <div>''' + "{}".format(dTmpl['bass_general_issues']) + '''</div>
                                    </div>'''
        var_html += '''
                                </div>
                            </div>
                            <div class="tab-pane" id="tab_guitar">
                                <div class="span12">'''
        if dTmpl['guitar_green_oranges_three'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Gem + G + O</h3>
                                        <div>''' + "{}".format(dTmpl['guitar_green_oranges_three']) + '''</div>
                                    </div>'''
        if dTmpl['guitar_chords_four_notes'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Four-Note Chords</h3>
                                        <div>''' + "{}".format(dTmpl['guitar_chords_four_notes']) + '''</div>
                                    </div>'''
        if dTmpl['guitar_chords_three_notes'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Three-Note Chords on Hard</h3>
                                        <div>''' + "{}".format(dTmpl['guitar_chords_three_notes']) + '''</div>
                                    </div>'''
        if dTmpl['guitar_chords_dont_exist'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Chord Difficulty Mismatch</h3>
                                        <div>''' + "{}".format(dTmpl['guitar_chords_dont_exist']) + '''</div>
                                    </div>'''
        if dTmpl['guitar_chords_h_green_orange'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">G+O Chords on Hard</h3>
                                        <div>''' + "{}".format(dTmpl['guitar_chords_h_green_orange']) + '''</div>
                                    </div>'''
        if dTmpl['guitar_chords_m_chord_combos'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">G+B / G+O / R+O Chords on Medium</h3>
                                        <div>''' + "{}".format(dTmpl['guitar_chords_m_chord_combos']) + '''</div>
                                    </div>'''
        if dTmpl['guitar_chords_m_hopos'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Forced HOPOs on Medium</h3>
                                        <div>''' + "{}".format(dTmpl['guitar_chords_m_hopos']) + '''</div>
                                    </div>'''
        if dTmpl['guitar_chords_easy'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Easy Chords</h3>
                                        <div>''' + "{}".format(dTmpl['guitar_chords_easy']) + '''</div>
                                    </div>'''
        if dTmpl['guitar_general_issues'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">General Errors / Warnings</h3>
                                        <div>''' + "{}".format(dTmpl['guitar_general_issues']) + '''</div>
                                    </div>'''

        var_html += '''
                                </div>
                            </div>
                            <div class="tab-pane" id="tab_rhythm">
                                <div class="span12">'''
        if dTmpl['rhythm_green_oranges_three'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Gem + G + O</h3>
                                        <div>''' + "{}".format(dTmpl['rhythm_green_oranges_three']) + '''</div>
                                    </div>'''
        if dTmpl['rhythm_chords_four_notes'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Four-Note Chords</h3>
                                        <div>''' + "{}".format(dTmpl['rhythm_chords_four_notes']) + '''</div>
                                    </div>'''
        if dTmpl['rhythm_chords_three_notes'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Three-Note Chords on Hard</h3>
                                        <div>''' + "{}".format(dTmpl['rhythm_chords_three_notes']) + '''</div>
                                    </div>'''
        if dTmpl['rhythm_chords_dont_exist'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Chord Difficulty Mismatch</h3>
                                        <div>''' + "{}".format(dTmpl['rhythm_chords_dont_exist']) + '''</div>
                                    </div>'''
        if dTmpl['rhythm_chords_h_green_orange'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">G+O Chords on Hard</h3>
                                        <div>''' + "{}".format(dTmpl['rhythm_chords_h_green_orange']) + '''</div>
                                    </div>'''
        if dTmpl['rhythm_chords_m_chord_combos'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">G+B / G+O / R+O Chords on Medium</h3>
                                        <div>''' + "{}".format(dTmpl['rhythm_chords_m_chord_combos']) + '''</div>
                                    </div>'''
        if dTmpl['rhythm_chords_m_hopos'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Forced HOPOs on Medium</h3>
                                        <div>''' + "{}".format(dTmpl['rhythm_chords_m_hopos']) + '''</div>
                                    </div>'''
        if dTmpl['rhythm_chords_easy'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Easy Chords</h3>
                                        <div>''' + "{}".format(dTmpl['rhythm_chords_easy']) + '''</div>
                                    </div>'''
        if dTmpl['rhythm_general_issues'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">General Errors / Warnings</h3>
                                        <div>''' + "{}".format(dTmpl['rhythm_general_issues']) + '''</div>
                                    </div>'''

        var_html += '''</div>
    
                            </div>
                            <div class="tab-pane" id="tab_prokeys">
                                <div class="span12">'''

        if dTmpl['real_keys_x_lane_shift_issues'] + dTmpl['real_keys_h_lane_shift_issues'] + dTmpl['real_keys_m_lane_shift_issues'] + dTmpl['real_keys_e_lane_shift_issues'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Lane Shift Issues</h3>
                                        <div>''' + "{}".format(dTmpl['real_keys_x_lane_shift_issues']) + '''</div>
                                        <div>''' + "{}".format(dTmpl['real_keys_h_lane_shift_issues']) + '''</div>
                                        <div>''' + "{}".format(dTmpl['real_keys_m_lane_shift_issues']) + '''</div>
                                        <div>''' + "{}".format(dTmpl['real_keys_e_lane_shift_issues']) + '''</div>
                                    </div>'''

        if dTmpl['real_keys_x_range_issues'] + dTmpl['real_keys_h_range_issues'] + dTmpl['real_keys_m_range_issues'] + dTmpl['real_keys_e_range_issues'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Range Issues</h3>
                                        <div>''' + "{}".format(dTmpl['real_keys_x_range_issues']) + '''</div>
                                        <div>''' + "{}".format(dTmpl['real_keys_h_range_issues']) + '''</div>
                                        <div>''' + "{}".format(dTmpl['real_keys_m_range_issues']) + '''</div>
                                        <div>''' + "{}".format(dTmpl['real_keys_e_range_issues']) + '''</div>
                                    </div>'''

        if dTmpl['real_keys_x_general_issues'] + dTmpl['real_keys_h_general_issues'] + dTmpl['real_keys_m_general_issues'] + dTmpl['real_keys_e_general_issues'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">General Issues</h3>
                                        <div>''' + "{}".format(dTmpl['real_keys_x_general_issues']) + '''</div>
                                        <div>''' + "{}".format(dTmpl['real_keys_h_general_issues']) + '''</div>
                                        <div>''' + "{}".format(dTmpl['real_keys_m_general_issues']) + '''</div>
                                        <div>''' + "{}".format(dTmpl['real_keys_e_general_issues']) + '''</div>
                                    </div>'''

        var_html += '''
                                </div>
                            </div>
                            <div class="tab-pane" id="tab_keys">
                                <div class="span12"> '''
        if dTmpl['keys_general_issues'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">General Issues</h3>
                                        <div>''' + "{}".format(dTmpl['keys_general_issues']) + '''</div>
                                    </div>'''
        if dTmpl['keys_gems_not_found'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Difficulty Note Mismatch</h3>
                                        <div>''' + "{}".format(dTmpl['keys_gems_not_found']) + '''</div>
                                    </div>'''
        if dTmpl['keys_chords_four_notes'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Four-Note Chords</h3>
                                        <div>''' + "{}".format(dTmpl['keys_chords_four_notes']) + '''</div>
                                    </div>'''
        if dTmpl['keys_chords_three_notes'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Three-Note Chords on Medium</h3>
                                        <div>''' + "{}".format(dTmpl['keys_chords_three_notes']) + '''</div>
                                    </div>'''
        if dTmpl['keys_chords_easy'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">Easy Chords</h3>
                                        <div>''' + "{}".format(dTmpl['keys_chords_easy']) + '''</div>
                                    </div>'''
        var_html += '''                            
                                </div>
    
                            </div>
                            <div class="tab-pane" id="tab_vocals">
                                <div class="span12">'''

        if len(dTmpl['vocals_od_start']) != len(dTmpl['harm1_od_start']):
            if 'harm1' in available_tracks:
                var_html += '''
                                    <div class="alert alert-error">
                                        <h3>Vocals Errors</h3>
                                        <div>- Number of OD phrases in PART VOCALS (''' + str(
                    len(dTmpl['vocals_od_start'])) + ''') is different than HARM1 (''' + str(len(dTmpl['harm1_od_start'])) + ''')</div>
                                    </div>
                '''
        else:
            for index, item in enumerate(dTmpl['vocals_od_start']):
                if item != dTmpl['harm1_od_start'][index] or dTmpl['vocals_od_end'][index] != dTmpl['harm1_od_end'][index]:
                    var_html += '''
                                <div class="alert alert-error">
                                    <h3>Vocals Errors (Overdrive)</h3>
                                    <div>
                                        ''' + "- Overdrive #{} in VOCALS [ Starts: {}, Ends: {} ] starts or ends in a different place than HARM1 [ Starts: {}, Ends: {} ]".format(
                        index + 1, format_location(item), format_location(dTmpl['vocals_od_end'][index]),
                        format_location(dTmpl['harm1_od_start'][index]), format_location(dTmpl['harm1_od_end'][index])) + '''
                                    </div>
                                </div>
                    '''
        if dTmpl['vocals_general_issues'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">General Issues</h3>
                                        <div>''' + "{}".format(dTmpl['vocals_general_issues']) + '''</div>
                                    </div>'''
        var_html += '''
                                    <h3 class="alert alert-info">Lyrics</h3>
                                    ''' + (dTmpl['vocals_phrases']) + '''
                                </div>
                            </div>
                            <div class="tab-pane" id="tab_harm1">
                                <div class="span12"> '''
        if dTmpl['harm1_general_issues'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">General Issues</h3>
                                        <div>''' + "{}".format(dTmpl['harm1_general_issues']) + '''</div>
                                    </div>'''
        var_html += '''
                                    <h3 class="alert alert-info">Lyrics</h3>
                                        ''' + (dTmpl['harm1_phrases']) + '''
                                </div>
    
                            </div>
                            <div class="tab-pane" id="tab_harm2">
                                <div class="span12"> '''
        if dTmpl['harm2_general_issues'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">General Issues</h3>
                                        <div>''' + "{}".format(dTmpl['harm2_general_issues']) + '''</div>
                                    </div>'''
        var_html += '''
                                <h3 class="alert alert-info">Lyrics</h3>
                                    ''' + (dTmpl['harm2_phrases']) + '''
                                </div>
    
                            </div>
                            <div class="tab-pane" id="tab_harm3">
                                <div class="span12"> '''
        if dTmpl['harm3_general_issues'] != '':
            var_html += '''
                                    <div>
                                        <h3 class="alert alert-error">General Issues</h3>
                                        <div>''' + "{}".format(dTmpl['harm3_general_issues']) + '''</div>
                                    </div>'''
        var_html += '''
                                <h3 class="alert alert-info">Lyrics</h3>
                                    ''' + (dTmpl['harm3_phrases']) + '''
                                </div>
    
                            </div>
                            <div class="tab-pane" id="tab_events">
                                <div class="span12"> 
                                <div class="lead"><h3>Event Types</h3></div>
                                '''
        if dTmpl['events_list'] != '':
            var_html += '''
                                    <div>                                    
                                        <div>''' + "{}".format(dTmpl['events_list']) + '''</div>
                                    </div>
                                    <table class="" id="" width="''' + "{}".format((int(dTmpl['last_event']) * 10)) + '''px">
                                        <tr>
                                        </tr>
                                    </table>
        '''
        var_html += '''
                                </div>                        
                            </div>
                            <div class="tab-pane" id="tab_venue">
                                <div class="span12"> 
            '''
        var_html += '''
                                </div>
                            </div>
                            <div class="tab-pane" id="tab_od">
                                <div class="span12">
                                    <div class="lead"><h3>Overdrive Visualizer</h3></div>
                                    <table class="table table-condensed" id="" width="''' + "{}".format(
            (int(dTmpl['last_event']) * 10)) + '''px">
                                '''
        for instrument in ['drums', 'drums_2x', 'bass', 'guitar', 'rhythm', 'keys']:
            full_ods = dTmpl[instrument + '_pos_od']
            if len(full_ods) > 0:
                if len(full_ods) < 1:
                    full_ods = []
                var_html += ''' <tr > 
                                                    <td>''' + instrument.title() + '''</td>
                                        '''
                for n in range(1, int(dTmpl['last_event'])):
                    if n in full_ods:
                        var_html += '''
                                                    <td width="10px" style="background-color:#D4A017" id="''' + "{}_{}".format(
                            instrument, n) + '''"><a href="#" title="''' + "Aprox. Position {}".format(
                            n) + '''" alt="''' + "Aprox. Position {}".format(n) + '''">...</a></td>
                                            '''
                    else:
                        var_html += '''
                                                    <td width="10px" style="" id="''' + "{}_{}".format(instrument, n) + '''"></td>
                                            '''
                var_html += ''' </tr> '''
        var_html += ''' </table> '''
        var_html += '''                    
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
        </div><!--/.fluid-container-->    
        <script src="js/jquery.js"></script>
        <script src="js/bootstrap.min.js"></script>
        </body>
    </html>
    '''

        f.write(var_html)

