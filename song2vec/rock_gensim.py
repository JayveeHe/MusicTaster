# coding=utf-8

"""
Created by jayvee on 17/2/16.
https://github.com/JayveeHe
"""
import gensim
import pickle
from gensim import corpora
from gensim.models import word2vec

from utils.cloudmusic_dao import CloudMusicDAO
from utils.logger_utils import data_process_logger


def prepare_song_dict(tag=''):
    """
    从数据库中遍历歌单,准备song2vec的训练数据
    Args:
        tag: 备注tag信息

    Returns:

    """
    playlist_dao_inst = CloudMusicDAO('MusicTaster', 'Playlists')
    print playlist_dao_inst.db_inst.find(
        {'trackCount': {'$gte': 3, '$lte': 1000}, 'playCount': {'$gte': 1}},
        {'tracks': 1, 'name': 1}).limit(100000).count()
    find_result = playlist_dao_inst.db_inst.find(
        {'trackCount': {'$gte': 3, '$lte': 1000}, 'playCount': {'$gte': 1}},
        {'tracks': 1, 'name': 1}).limit(100000)
    # 将歌单中的歌曲名组合成歌曲名序列
    total_song_set = []
    count = 0
    for item in find_result:
        data_process_logger.info('No.%s %s' % (count, item['name']))
        # 保存歌单中的歌曲序列
        song_seq = []
        for song in item['tracks']:
            sname = song['name']
            song_seq.append(sname.lower())
        total_song_set.append(song_seq)
        count += 1
    data_process_logger.info('start building dictionary')
    song_dictionary = corpora.Dictionary(total_song_set)
    print u'歌单数', song_dictionary.num_docs
    print u'歌曲数', song_dictionary.num_pos
    data_process_logger.info('start saving datas')
    song_dictionary.save('../datas/song_dictionary_%s.dict' % tag)
    pickle.dump(total_song_set, open('../datas/songs_seq_%s.dat' % tag, 'wb'))
    return song_dictionary


def train_song2vec_model(fout_path, input_datas=None, data_path=None, min_count=5, sorted_vocab=1, window=10, size=250,
                         iter_n=50):
    """
    训练song2vec模型
    Args:
        fout_path:
        input_datas:
        data_path:
        min_count:
        sorted_vocab:
        window:
        size:
        iter_n:

    Returns:

    """
    if not input_datas and data_path:
        input_datas = pickle.load(open(data_path, 'rb'))
    data_process_logger.info('start training')
    wv_model = gensim.models.Word2Vec(input_datas, min_count=min_count, sorted_vocab=sorted_vocab, window=window,
                                      size=size, iter=iter_n)
    with open(fout_path, 'wb') as fout:
        data_process_logger.info('start saving model')
        pickle.dump(wv_model, fout)
        print 'model saved'


def prepare_artist_dict(tag=''):
    playlist_dao_inst = CloudMusicDAO('MusicTaster', 'Playlists')
    # print playlist_dao_inst.db_inst.find(
    #     {'trackCount': {'$gte': 10, '$lte': 600}, 'playCount': {'$gte': 10}},
    #     {'name': 1}).limit(100000).count()
    find_result = playlist_dao_inst.db_inst.find(
        {'trackCount': {'$gte': 10, '$lte': 600}, 'playCount': {'$gte': 5}},
        {'tracks': 1, 'name': 1}).limit(100000)
    # 将歌单中的歌曲名组合成歌曲名序列
    total_artists_set = []
    count = 0
    for item in find_result:
        data_process_logger.info('No.%s %s' % (count, item['name']))
        # 保存歌单中的歌曲序列
        artists_seq = []
        for song in item['tracks']:
            sname = song['artists'][0]['name']
            artists_seq.append(sname.lower())
        total_artists_set.append(artists_seq)
        count += 1
    data_process_logger.info('start building dictionary')
    artist_dictionary = corpora.Dictionary(total_artists_set)
    print u'歌单数', artist_dictionary.num_docs
    try:
        print u'歌手数', len(artist_dictionary.token2id)
    except Exception, e:
        print 'error = %s' % e
    data_process_logger.info('start saving datas')
    artist_dictionary.save('../datas/artists_dictionary_%s.dict' % tag)
    pickle.dump(total_artists_set, open('../datas/artists_seq_%s.dat' % tag, 'wb'))
    return artist_dictionary


def train_artist2vec_model(fout_path, input_datas=None, data_path=None, min_count=5, sorted_vocab=1, window=10,
                           size=250,
                           iter_n=50):
    if not input_datas and data_path:
        input_datas = pickle.load(open(data_path, 'rb'))
    data_process_logger.info('start training')
    wv_model = gensim.models.Word2Vec(input_datas, min_count=min_count, sorted_vocab=sorted_vocab, window=window,
                                      size=size, iter=iter_n)
    with open(fout_path, 'wb') as fout:
        data_process_logger.info('start saving model')
        pickle.dump(wv_model, fout)
        print 'model saved'


def train_artistsong2vec_model(fout_path, input_datas=None, data_path=None,
                               min_count=5, sorted_vocab=1, window=10,
                               size=250,
                               iter_n=50):
    if not input_datas and data_path:
        input_datas = pickle.load(open(data_path, 'rb'))
    full_data = []
    for i in input_datas:
        tmp = []
        for j in i:
            tmp.append(j[0])
            tmp.append(j[1])
        full_data.append(tmp)
    data_process_logger.info('start training')
    wv_model = gensim.models.Word2Vec(full_data, min_count=min_count, sorted_vocab=sorted_vocab, window=window,
                                      size=size, iter=iter_n)
    with open(fout_path, 'wb') as fout:
        data_process_logger.info('start saving model')
        pickle.dump(wv_model, fout)
        print 'model saved'


def test_song2vec():
    tag = 'full'
    # prepare_song_dict(tag=tag)
    min_count = 5
    sorted_vocab = 1
    window = 10
    size = 50
    iter_n = 20
    modelpath = '../datas/[%s]%sd_%siter_%swin_%smin_song2vec.model' % (tag, size, iter_n, window, min_count)
    # train_song2vec_model(fout_path=modelpath, data_path='../datas/songs_seq_%s.dat' % tag,
    #                      min_count=min_count,
    #                      sorted_vocab=sorted_vocab, window=window,
    #                      size=size, iter_n=iter_n)
    print 'model params:\tag: %s\tnmin: %s\twin: %s\tsize: %s\titer_n: %s' % (tag, min_count, window, size, iter_n)
    with open(modelpath, 'rb') as fin:
        data_process_logger.info('loading')
        m = pickle.load(fin)
        data_process_logger.info('start predicting')
        s1, s2 = u'半岛铁盒', u'成都'.lower()
        print u'%s 与 %s 的相似度为: %.4f' % (s1, s2, m.similarity(s1, s2))
        s1, s2 = u'viva la vida', u'yellow'
        print u'%s 与 %s 的相似度为: %.4f' % (s1, s2, m.similarity(s1, s2))
        s1, s2 = u'夜空中最亮的星', u'南山南'
        print u'%s 与 %s 的相似度为: %.4f' % (s1, s2, m.similarity(s1, s2))
        s1, s2 = u'photograph', u'need you now'
        print u'%s 与 %s 的相似度为: %.4f' % (s1, s2, m.similarity(s1, s2))
        print '---------------'
        tsong = u'告白气球'
        print u'%s 最相似的歌曲:' % tsong
        for i in m.most_similar(tsong, topn=20):
            print i[0], i[1]
        print '---------------'
        tsong = u'晴天'.lower()
        print u'%s 最相似的歌曲:' % tsong
        for i in m.most_similar(tsong, topn=20):
            print i[0], i[1]
        print '---------------'
        tsong = u'are you ok'.lower()
        print u'%s 最相似的歌曲:' % tsong
        for i in m.most_similar(tsong, topn=20):
            print i[0], i[1]
        print '---------------'
        tsong = u'How To Save A Life - New Album Version'.lower()
        print u'%s 最相似的歌曲:' % tsong
        for i in m.most_similar(tsong, topn=20):
            print i[0], i[1]
        print '---------------'
        tsong = u'往南'.lower()
        print u'%s 最相似的歌曲:' % tsong
        for i in m.most_similar(tsong, topn=20):
            print i[0], i[1]
        print '=============='
        add_arr = [u'晴天', u'雨天', u'欧若拉']
        minus_arr = [u'说爱你']
        line = '+'.join(add_arr)
        line += '-' + '-'.join(minus_arr)
        print line
        for i in m.most_similar(positive=add_arr, negative=minus_arr):
            print i[0], i[1]


def test_artist2vec():
    tag = 'full'
    min_count = 5
    sorted_vocab = 1
    window = 10
    size = 50
    iter_n = 20
    # prepare_artist_dict(tag=tag)
    modelpath = '../datas/[%s]%sd_%siter_%swin_%smin_artist2vec.model' % (tag, size, iter_n, window, min_count)
    print 'model params:\tag: %s\tnmin: %s\twin: %s\tsize: %s\titer_n: %s' % (tag, min_count, window, size, iter_n)
    # train_artist2vec_model(fout_path=modelpath, data_path='../datas/artists_seq_%s.dat' % tag,
    #                        min_count=min_count,
    #                        sorted_vocab=sorted_vocab, window=window,
    #                        size=size, iter_n=iter_n)
    with open(modelpath, 'rb') as fin:
        m = pickle.load(fin)
        s1, s2 = u'周杰伦', u'王力宏'.lower()
        print u'%s 与 %s 的相似度为: %.4f' % (s1, s2, m.similarity(s1, s2))
        s1, s2 = u'蔡依林', u'梁静茹'
        print u'%s 与 %s 的相似度为: %.4f' % (s1, s2, m.similarity(s1, s2))
        s1, s2 = u'梁静茹', u'孙燕姿'
        print u'%s 与 %s 的相似度为: %.4f' % (s1, s2, m.similarity(s1, s2))
        print '---------------'
        tsong = u'老狼'
        print u'%s 最相似的歌手:' % tsong
        for i in m.most_similar(tsong, topn=20):
            print i[0], i[1]
        print '---------------'
        tsong = u'周杰伦'.lower()
        print u'%s 最相似的歌手:' % tsong
        for i in m.most_similar(tsong, topn=20):
            print i[0], i[1]
        print '---------------'
        tsong = u'蔡依林'.lower()
        print u'%s 最相似的歌手:' % tsong
        for i in m.most_similar(tsong, topn=20):
            print i[0], i[1]
        print '---------------'
        tsong = u's.h.e'.lower()
        print u'%s 最相似的歌手:' % tsong
        for i in m.most_similar(tsong, topn=20):
            print i[0], i[1]
        print '---------------'
        tsong = u'spyair'.lower()
        print u'%s 最相似的歌手:' % tsong
        for i in m.most_similar(tsong, topn=20):
            print i[0], i[1]
        print '=============='
        # add_arr = [u'晴天', u'布拉格广场', u'去大理']
        # minus_arr = [u'faded'.lower(), u'时间煮雨', u'爱的供养']
        # line = '+'.join(add_arr)
        # line += '-' + '-'.join(minus_arr)
        # print line
        # for i in m.most_similar(positive=add_arr, negative=minus_arr):
        #     print i[0], i[1]


def prepare_song_artist_dict(tag=''):
    playlist_dao_inst = CloudMusicDAO('MusicTaster', 'Playlists')
    print playlist_dao_inst.db_inst.find(
        {'trackCount': {'$gte': 5, '$lte': 1000}, 'playCount': {'$gte': 5}},
        {'tracks': 1, 'name': 1}).limit(100000).count()
    find_result = playlist_dao_inst.db_inst.find(
        {'trackCount': {'$gte': 5, '$lte': 1000}, 'playCount': {'$gte': 5}},
        {'tracks': 1, 'name': 1}).limit(100000)
    # 将歌单中的歌曲名组合成歌曲名序列
    total_song_artist_set = []
    count = 0
    for item in find_result:
        data_process_logger.info('No.%s %s' % (count, item['name']))
        # 保存歌单中的歌曲序列
        song_artist_seq = []
        for song in item['tracks']:
            sname = song['name']
            artist = song['artists'][0]['name'].lower()
            song_artist_seq.append((sname.lower(), artist))
        total_song_artist_set.append(song_artist_seq)
        count += 1
    data_process_logger.info('start building dictionary')
    # song_dictionary = corpora.Dictionary(total_song_artist_set)
    # print u'歌单数', song_dictionary.num_docs
    # print u'歌曲数', song_dictionary.num_pos
    data_process_logger.info('start saving datas')
    # song_dictionary.save('../datas/song_artist_dictionary_%s.dict' % tag)
    pickle.dump(total_song_artist_set, open('../datas/songs_artists_seq_%s.dat' % tag, 'wb'))
    # return song_dictionary


def test_artistsong2vec():
    tag = 'full'
    min_count = 5
    sorted_vocab = 1
    window = 10
    size = 50
    iter_n = 20
    # prepare_artist_dict(tag=tag)
    modelpath = '../datas/[%s]%sd_%siter_%swin_%smin_artistsong2vec.model' % (tag, size, iter_n, window, min_count)
    print 'model params:\tag: %s\tnmin: %s\twin: %s\tsize: %s\titer_n: %s' % (tag, min_count, window, size, iter_n)
    # train_artistsong2vec_model(fout_path=modelpath, data_path='../datas/songs_artists_seq_%s.dat' % tag)
    with open(modelpath, 'rb') as fin:
        m = pickle.load(fin)
        s1, s2 = u'周杰伦', u'蔡依林'.lower()
        print u'%s 与 %s 的相似度为: %.4f' % (s1, s2, m.similarity(s1, s2))
        s1, s2 = u'周杰伦', u'东风破'
        print u'%s 与 %s 的相似度为: %.4f' % (s1, s2, m.similarity(s1, s2))
        s1, s2 = u'梁静茹', u'孙燕姿'
        print u'%s 与 %s 的相似度为: %.4f' % (s1, s2, m.similarity(s1, s2))
        print '---------------'
        tsong = u'你听得到'
        print u'%s 最相似的歌手:' % tsong
        for i in m.most_similar(tsong, topn=20):
            print i[0], i[1]
        print '---------------'
        tsong = u'周杰伦'.lower()
        print u'%s 最相似的歌手:' % tsong
        for i in m.most_similar(tsong, topn=20):
            print i[0], i[1]
        print '---------------'
        tsong = u'蔡依林'.lower()
        print u'%s 最相似的歌手:' % tsong
        for i in m.most_similar(tsong, topn=20):
            print i[0], i[1]
        print '---------------'
        tsong = u'雷军'.lower()
        print u'%s 最相似的歌手:' % tsong
        for i in m.most_similar(tsong, topn=20):
            print i[0], i[1]
        print '---------------'
        tsong = u'王力宏'.lower()
        print u'%s 最相似的歌手:' % tsong
        for i in m.most_similar_cosmul(tsong, topn=20):
            print i[0], i[1]
        print '=============='
        add_arr = [u'周杰伦', u'王力宏', u'王力宏']
        minus_arr = [u'晴天', u'回到过去']
        line = '+'.join(add_arr)
        line += '-' + '-'.join(minus_arr)
        print line
        for i in m.most_similar(positive=add_arr, negative=minus_arr):
            print i[0], i[1]


if __name__ == '__main__':
    test_song2vec()
    # test_artist2vec()
    # prepare_song_artist_dict('full')
    # test_artistsong2vec()
