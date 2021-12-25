import 'dart:async';
import 'dart:math';
import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersive);
  SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);
  return runApp(
    const MaterialApp(home: Mimzy(), debugShowCheckedModeBanner: false),
  );
}

class Mimzy extends StatefulWidget {
  const Mimzy({Key? key}) : super(key: key);

  @override
  _MimzyState createState() => _MimzyState();
}

Size screenSize = Size.zero;
Offset? forceField;
int way = -1, forceVal = 0;
List<Point> _points = [];
Random r = Random();
double getR() => r.nextDouble() - 0.5;
const int particleCount = 250;

class _MimzyState extends State<Mimzy> {
  Offset getDelta(Offset delta, double n, double way) =>
      (Offset(n * delta.dx.sign, n * delta.dy.sign) - delta) * way;

  @override
  Widget build(BuildContext context) {
    if (screenSize == Size.zero) {
      screenSize = MediaQuery.of(context).size;
      _points = List.generate(particleCount, (_) => Point());
      Timer.periodic(
          const Duration(milliseconds: 17),
          (_) => setState(() {
                if (forceField != null) {
                  for (Point z in _points) {
                    Offset delta = forceField! - z.pos;
                    if (delta.distanceSquared < 4000) {
                      z.velocity += getDelta(delta, 4000, way.toDouble()) / 1500;
                      z.magnetism = way;
                    }
                  }
                }
                for (Point p in _points) {
                  for (Point z in _points) {
                    Offset delta = p.pos - z.pos;
                    if (delta.distanceSquared < 1600 * p.mass) {
                      z.velocity += getDelta(delta, 1600, p.magnetism * p.mass) / 5000;
                    }
                  }
                }
              }));
    }
    return GestureDetector(
      onPanStart: moveForceField,
      onPanUpdate: moveForceField,
      onPanEnd: (_) => forceField = null,
      onDoubleTap: () {
        way *= -1;
        forceVal = (way < 0) ? 0x88cc0000 : 0x880000cc;
      },
      onLongPress: () => _points = _points.map((e) => e..magnetism = way).toList(),
      child: CustomPaint(painter: MyPainter()),
    );
  }

  moveForceField(p) => forceField = p.globalPosition;
}

class MyPainter extends CustomPainter {
  final Paint _paint = Paint();

  @override
  void paint(Canvas canvas, Size size) {
    if (forceVal > 0x04000000) {
      canvas.drawColor(Color(forceVal), BlendMode.color);
      forceVal -= 0x04000000;
    }
    for (Point p in _points) {
      p.update();
      canvas.drawPoints(
          PointMode.points,
          [p.pos],
          _paint
            ..strokeWidth = p.mass
            ..color = (p.magnetism > 0) ? Colors.blue : Colors.red);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}

class Point {
  Offset pos = Offset(r.nextDouble() * screenSize.width, r.nextDouble() * screenSize.height);
  Offset velocity = Offset(getR(), getR());
  int magnetism = getR().sign.toInt();
  double mass = (r.nextDouble() + 0.2) * 2;

  update() {
    pos += velocity;
    velocity *= 0.9;
    bool xx = pos.dx > screenSize.width;
    bool yy = pos.dy > screenSize.height;
    if (pos.dx < 0 || xx) {
      pos = Offset((xx) ? screenSize.width - 2 : 2, pos.dy);
      velocity = velocity.scale(-1, 1);
    }
    if (pos.dy < 0 || yy) {
      pos = Offset(pos.dx, (yy) ? screenSize.height - 2 : 2);
      velocity = velocity.scale(1, -1);
    }
  }
}
