//not really accurate but close enough to look cool
//can't quite get the electrons to behave right

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


<!DOCTYPE html>
<html>
  <head>
    <style>
    img {
      clip-path: url(#shape);
      width: 18em;
      height: 18em;
      object-fit: cover;
      display: block;
      margin-right: auto;
      margin-left: auto;
    }
    </style>
  </head>
  <body>
    <img src="jesusCat.png" >    
      <svg width="0" height="0">
      <defs>
        <clipPath id="shape" clipPathUnits="objectBoundingBox">
          <path fill="none" d="M 0.3 0.6 L 0.75 0.075 L 0.975 0 L 0.9 0.225 L 0.375 0.675 C 0.45 0.75 0.45 0.825 0.525 0.75 C 0.525 0.825 0.6 0.9 0.525 0.9 A 0.1065 0.1065 90 0 1 0.45 0.975 A 0.375 0.375 90 0 0 0.3 0.75 Q 0.2625 0.7425 0.2625 0.7875 T 0.15 0.885 T 0.09 0.825 T 0.1875 0.7125 T 0.225 0.675 A 0.375 0.375 90 0 0 0 0.525 A 0.1065 0.1065 90 0 1 0.075 0.45 C 0.075 0.375 0.15 0.45 0.225 0.3 C 0.15 0.525 0.225 0.525 0.3 0.6 M 0.75 0.075 L 0.714 0.258 L 0.9 0.225 L 0.795 0.189 L 0.75 0.075"/>
        </clipPath>
      </defs>
    </svg>
  </body>
</html>


