'''
Fix pg.graphicsItems.ViewBox.enableAutoRange method
'''

import pyqtgraph as pg
import numpy as np

def updateAutoRange(self):
    ## Break recursive loops when auto-ranging.
    ## This is needed because some items change their size in response
    ## to a view change.
    if self._updatingRange:
        return

    self._updatingRange = True
    try:
        targetRect = self.viewRange()
        if not any(self.state['autoRange']):
            return

        fractionVisible = self.state['autoRange'][:]
        for i in [0,1]:
            if type(fractionVisible[i]) is bool:
                fractionVisible[i] = 1.0

        childRange = None

        order = [0,1]
        if self.state['autoVisibleOnly'][0] is True:
            order = [1,0]

        args = {}
        for ax in order:
            if self.state['autoRange'][ax] is False:
                continue
            if self.state['autoVisibleOnly'][ax]:
                oRange = [None, None]
                oRange[ax] = targetRect[1-ax]
                childRange = self.childrenBounds(frac=fractionVisible, orthoRange=oRange)

            else:
                if childRange is None:
                    childRange = self.childrenBounds(frac=fractionVisible)

            ## Make corrections to range
            xr = childRange[ax]
            if xr is not None:
                if self.state['autoPan'][ax]:
                    # x = sum(xr) * 0.5
                    # w2 = (targetRect[ax][1]-targetRect[ax][0]) / 2.
                    w = (targetRect[ax][1]-targetRect[ax][0])
                    childRange[ax] = [xr[1]-w, xr[1]]
                    # childRange[ax] = [x-w2, x+w2]
                else:
                    padding = self.suggestPadding(ax)
                    wp = (xr[1] - xr[0]) * padding
                    childRange[ax][0] -= wp
                    childRange[ax][1] += wp
                targetRect[ax] = childRange[ax]
                args['xRange' if ax == 0 else 'yRange'] = targetRect[ax]
        if len(args) == 0:
            return
        args['padding'] = 0
        args['disableAutoRange'] = False

         # check for and ignore bad ranges
        for k in ['xRange', 'yRange']:
            if k in args:
                if not np.all(np.isfinite(args[k])):
                    r = args.pop(k)
                    #print("Warning: %s is invalid: %s" % (k, str(r))

        self.setRange(**args)
    finally:
        self._autoRangeNeedsUpdate = False
        self._updatingRange = False


pg.graphicsItems.ViewBox.ViewBox.updateAutoRange_old = pg.graphicsItems.ViewBox.ViewBox.updateAutoRange
pg.graphicsItems.ViewBox.ViewBox.updateAutoRange = updateAutoRange