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
List<Particle> electrons = [], neutrons = [], protons = [];
Offset? forceField;

class _MimzyState extends State<Mimzy> {
  Offset force(Offset delta) => Offset.fromDirection(delta.direction, 5 / (delta.distanceSquared + 1));

  strongForce(Particle p1, Particle p2) {
    Offset d = p1.pos - p2.pos;
    if (d.distanceSquared < 150) {
      Offset z = force(d) * 250;
      p1.velocity -= z;
      p2.velocity += z;
    }
  }

  @override
  Widget build(BuildContext context) {
    if (screenSize == Size.zero) {
      screenSize = MediaQuery.of(context).size;
      electrons = List.generate(150, (_) => Particle());
      neutrons = List.generate(150, (_) => Particle());
      protons = List.generate(150, (_) => Particle());
      Timer.periodic(
        const Duration(milliseconds: 33),
        (t) => setState(
          () {
            if (forceField != null) {
              for (Particle p in electrons + neutrons + protons) {
                p.velocity += force(forceField! - p.pos) * 4000;
              }
            }
            for (Particle p in protons) {
              for (Particle p2 in protons) {
                if (p != p2) p.velocity += force(p.pos - p2.pos);
                strongForce(p, p2);
              }
              for (Particle n in neutrons) {
                strongForce(p, n);
              }
              for (Particle e in electrons) {
                e.velocity -= force(e.pos - p.pos) * 75;
              }
            }
            for (Particle e in electrons) {
              for (Particle e2 in electrons) {
                if (e != e2) e.velocity += force(e.pos - e2.pos) * 75;
              }
            }
          },
        ),
      );
    }
    return GestureDetector(
        onPanStart: moveForceField,
        onPanUpdate: moveForceField,
        onPanEnd: (_) => forceField = null,
        child: CustomPaint(painter: MyPainter()));
  }

  moveForceField(p) => forceField = p.globalPosition;
}

class MyPainter extends CustomPainter {
  final Paint _paint = Paint();
  drawParticleList(Canvas canvas, List<Particle> pList, double mass, Color c) {
    canvas.drawPoints(
      PointMode.points,
      pList.map((p) {
        p.update();
        return p.pos;
      }).toList(),
      _paint
        ..strokeWidth = mass
        ..color = c,
    );
  }

  @override
  void paint(Canvas canvas, Size size) {
    drawParticleList(canvas, electrons, 1.5, const Color(0xff0000ff));
    drawParticleList(canvas, neutrons, 2, const Color(0xffffffff));
    drawParticleList(canvas, protons, 2.1, const Color(0xffff0000));
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}

Random r = Random();
double getR() => r.nextDouble() - 0.5;

class Particle {
  Offset pos = Offset(r.nextDouble() * screenSize.width, r.nextDouble() * screenSize.height);
  Offset velocity = Offset(getR(), getR()) * 2;

  update() {
    velocity = Offset.fromDirection(velocity.direction, min(10, velocity.distance));
    pos += velocity;
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


// N 1839 0
// P 1836 1
// E 1   -1
