from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

class UserSimilarity(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    ###
    # TODO: write the functions needed to
    # 1) find potential matches,
    # 2) calculate the Jaccard between users, with a user defined as a set of
    # reviewed businesses
    ##/

    def extract_user_business(self, _, record):
        if record['type'] == 'review':
            yield [record['user_id'], record['business_id']]

    def get_num_unique_reviews(self, uid, bids):
        # key things by bid, rename uids with the number of businesses they reviewed
        bids = set(bids)
        for bid in bids:
            yield [bid, [uid, len(bids)]]

    def get_user_pairings(self, bid, uinfos):
        for u1 in uinfos:
            for u2 in uinfos:
                if u1[0] != u2[0]:
                    pairing = [u1, u2]
                    # to ensure proper grouping
                    pairing.sort()
                    yield [pairing, bid]

    def group_bids(self, uinfos, bids):
        yield[uinfos, list(set(bids))]

    def get_jaccard(self, uinfos, bids):
        intersection = len(bids)
        superunion = uinfos[0][1] + uinfos[1][1]
        union = superunion - intersection
        jaccard = intersection / float(union)
        if (jaccard >= 0.5):
            yield [[uinfos[0][0], uinfos[1][0]], jaccard]

    def steps(self):
        """TODO: Document what you expect each mapper and reducer to produce:
        mapper1: <line, record> => <user, business>
        reducer1: <user, [businesses]> => <business, [user, num_of_unique_business_reviewed]>
        reducer2: <business, [user, num_of_unique_businesses_reviewed]s> => <<[u1, num1], [u2, num2]>, business>
        reducer3: <<[u1, num1], [u2, num2]>, [businesses]>
        mapper2: <<u1, u2>, jaccard>
        """
        return [self.mr(mapper=self.extract_user_business, reducer=self.get_num_unique_reviews),
                self.mr(reducer=self.get_user_pairings),
                self.mr(reducer=self.group_bids),
                self.mr(mapper=self.get_jaccard)
                ]


if __name__ == '__main__':
    UserSimilarity.run()
