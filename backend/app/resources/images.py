
import random

from .base import BaseResource


class Images(BaseResource):

    def get(self, image_type):
        images = ['https://img.meikew.com/uploads/mw690/006tTKPugy1fd8mozkplrj30j60ecqkx.jpg',
                  'https://img.meikew.com/uploads/2017/10/170114rsfzrror3rss5oo6.png',
                  'https://img.meikew.com/uploads/2017/09/1027573w5k33qqub5nqcwq.jpg',
                  'https://img.meikew.com/uploads/2017/09/1610257d0is2vx7dvpsjdy.jpg',
                  ]

        images = ['http://ac-hcebow9l.clouddn.com/a1b8a4cf6fdb7475ad05.jpg'
                  ]

        return random.choice(images)
