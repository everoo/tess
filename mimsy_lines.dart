import 'dart:async';
import 'dart:math';
import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:sensors/sensors.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersive);
  SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);
  accelerometerEvents.listen((a) => gravity += Offset(-a.x, a.y) / 50);
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
Offset gravity = Offset.zero;
double way = -1;
List<Point> _points = [];
List<Offset> _lines = [];
Random r = Random();
double getR() => r.nextDouble() - 0.5;
Offset getDelta(Offset delta, double n, double s) =>
    (Offset(n * delta.dx.sign, n * delta.dy.sign) - delta) * s;

int forceVal = 0;

class _MimzyState extends State<Mimzy> {
  @override
  Widget build(BuildContext context) {
    if (screenSize == Size.zero) {
      screenSize = MediaQuery.of(context).size;
      _points = List.generate(340, (_) => Point());
      Timer.periodic(const Duration(milliseconds: 17), (t) {
        if (forceField != null) {
          for (Point z in _points) {
            Offset delta = forceField! - z.pos;
            if (delta.distanceSquared < 4000) {
              z.velocity += getDelta(delta, 4000, way) / 1000;
              z.magnetism = way;
            }
          }
        }
        _lines.clear();
        for (Point p in _points) {
          for (Point z in _points) {
            Offset delta = p.pos - z.pos;
            if (delta.distanceSquared < 1600) {
              _lines.addAll([p.pos, z.pos]);
              z.velocity += getDelta(delta, 1600, p.magnetism) / 4000;
            }
          }
          p.update();
        }
        if (forceVal > 0x04000000) forceVal -= 0x04000000;
        setState(() => gravity *= 0.93);
      });
    }
    return GestureDetector(
      onPanStart: moveForceField,
      onPanUpdate: moveForceField,
      onPanEnd: (_) => forceField = null,
      onDoubleTap: () {
        way *= -1;
        forceVal = (way == -1) ? 0x88cc0000 : 0x880000cc;
      },
      onLongPress: () {
        for (Point p in _points) {
          p.magnetism = way;
        }
      },
      child: CustomPaint(painter: MyPainter()),
    );
  }

  moveForceField(p) => forceField = p.globalPosition;
}

class MyPainter extends CustomPainter {
  final Paint _paint = Paint()
    ..strokeWidth = 1
    ..color = const Color(0xff22bb22);

  @override
  void paint(Canvas canvas, Size size) {
    if (forceVal > 0x04000000) canvas.drawColor(Color(forceVal), BlendMode.color);
    canvas.drawPoints(PointMode.lines, _lines, _paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}

class Point {
  Offset pos = Offset(r.nextDouble() * screenSize.width, r.nextDouble() * screenSize.height);
  Offset velocity = Offset(getR(), getR()) * 3;
  double magnetism = r.nextDouble() * 2 - 1;

  update() {
    velocity += gravity;
    velocity *= 0.95;
    pos += velocity;
    _checkEdges();
  }

  _checkEdges() {
    if (pos.dx < 0) {
      pos = Offset(2, pos.dy);
      velocity = velocity.scale(-1, 1);
    } else if (pos.dx > screenSize.width) {
      pos = Offset(screenSize.width - 2, pos.dy);
      velocity = velocity.scale(-1, 1);
    }
    if (pos.dy < 0) {
      pos = Offset(pos.dx, 2);
      velocity = velocity.scale(1, -1);
    } else if (pos.dy > screenSize.height) {
      pos = Offset(pos.dx, screenSize.height - 2);
      velocity = velocity.scale(1, -1);
    }
  }
}
