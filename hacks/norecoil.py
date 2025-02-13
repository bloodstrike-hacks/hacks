# THIS DISABLES AIM ASSIT AS WELL, FIND A BETTER WAY

from gclient.framework.camera.fps_placer import FpsPlacer
FpsPlacer.OnRecoilEnter = lambda *_, **__: None
