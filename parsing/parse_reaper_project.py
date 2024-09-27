import C3notes
from collections import defaultdict
from reaper_python import RPR_CountMediaItems, RPR_GetMediaItem, RPR_GetMediaItem_Track, RPR_GetSetMediaTrackInfo_String, RPR_GetSetItemState, RPR_ShowConsoleMsg


max_len = 1048576


def get_track_id_map():
    num_mi = RPR_CountMediaItems(0)

    track_id_map = defaultdict(lambda: 999)
    for idx in range(num_mi):
        media_item = RPR_GetMediaItem(0, idx)
        track_id = RPR_GetMediaItem_Track(media_item)
        track_name = RPR_GetSetMediaTrackInfo_String(track_id, "P_NAME", "", 0)[3]
        RPR_GetSetItemState(media_item, '', max_len)

        if track_name in C3notes.notesname_instruments_array.keys():
            track_id_map[track_name] = idx
        elif track_name in ['EVENTS', 'BEAT', 'VENUE']:
            track_id_map[track_name] = idx
        elif track_name in ["PART DRUMS 2x", "PART DRUMS_2x", "PART DRUMS_2X"]:
            RPR_ShowConsoleMsg(f'Warning: Please use track name \'PART DRUMS 2X\' instead of {track_name}')
            track_id_map['PART DRUMS 2X'] = idx

    return track_id_map
