class TrapezoidalFin {
    constructor(rootTip, rootEnd, semiSpan, tipChord, sweep, thickness, numberOfSegmentsChordwise, numberOfSegmentsSpanwise) {
        this.triangles = [];
        this.rootVector = new THREE.Vector3().subVectors(rootEnd, rootTip);
        this.rootChord = this.rootVector.length();
        this.sweepVector = this.rootVector.clone().multiplyScalar(sweep / this.rootVector.length());
        this.thicknessVector = new THREE.Vector3().crossVectors(this.rootVector, semiSpan).normalize();
        for(let s = 0; s < numberOfSegmentsSpanwise; s++) {
            let stripInsideTip = rootTip
                .clone()
                .add(semiSpan.clone().multiplyScalar(s / numberOfSegmentsSpanwise))
                .add(this.sweepVector.clone().multiplyScalar(s / numberOfSegmentsSpanwise));
            let stripOutsideTip = rootTip
                .clone()
                .add(semiSpan.clone().multiplyScalar((s + 1) / numberOfSegmentsSpanwise))
                .add(this.sweepVector.clone().multiplyScalar((s + 1) / numberOfSegmentsSpanwise));
            let elementInsideChord = (this.rootChord + (s / numberOfSegmentsSpanwise) * (tipChord - this.rootChord)) / numberOfSegmentsChordwise;
            let elementOutsideChord = (this.rootChord + ((s + 1) / numberOfSegmentsSpanwise) * (tipChord - this.rootChord)) / numberOfSegmentsChordwise;
            for(let c = 0; c < numberOfSegmentsChordwise; c++) {
                let elementInsideTip = stripInsideTip
                    .clone()
                    .add(this.rootVector.clone().normalize().multiplyScalar(elementInsideChord).multiplyScalar(c))
                    .add(this.thicknessVector.clone().multiplyScalar(thickness / 2.0));
                let elementInsideEnd = stripInsideTip
                    .clone()
                    .add(this.rootVector.clone().normalize().multiplyScalar(elementInsideChord).multiplyScalar(c + 1))
                    .add(this.thicknessVector.clone().multiplyScalar(thickness / 2.0));
                let elementOutsideTip = stripOutsideTip
                    .clone()
                    .add(this.rootVector.clone().normalize().multiplyScalar(elementOutsideChord).multiplyScalar(c))
                    .add(this.thicknessVector.clone().multiplyScalar(thickness / 2.0));
                let elementOutsideEnd = stripOutsideTip
                    .clone()
                    .add(this.rootVector.clone().normalize().multiplyScalar(elementOutsideChord).multiplyScalar(c + 1))
                    .add(this.thicknessVector.clone().multiplyScalar(thickness / 2.0));
                if(c == 0) {
                    elementInsideTip.sub(this.thicknessVector.clone().multiplyScalar(thickness / 2.0));
                    elementOutsideTip.sub(this.thicknessVector.clone().multiplyScalar(thickness / 2.0));
                }
                if(c == (numberOfSegmentsChordwise - 1)) {
                    elementInsideEnd.sub(this.thicknessVector.clone().multiplyScalar(thickness / 2.0));
                    elementOutsideEnd.sub(this.thicknessVector.clone().multiplyScalar(thickness / 2.0));
                }
                this.triangles.push(new Triangle(
                    elementInsideTip.toArray(),
                    elementInsideEnd.toArray(),
                    elementOutsideEnd.toArray()
                ));
                this.triangles.push(new Triangle(
                    elementInsideTip.toArray(),
                    elementOutsideEnd.toArray(),
                    elementOutsideTip.toArray()
                ));
            }
        }
        for(let s = 0; s < numberOfSegmentsSpanwise; s++) {
            let stripInsideTip = rootTip
                .clone()
                .add(semiSpan.clone().multiplyScalar(s / numberOfSegmentsSpanwise))
                .add(this.sweepVector.clone().multiplyScalar(s / numberOfSegmentsSpanwise));
            let stripOutsideTip = rootTip
                .clone()
                .add(semiSpan.clone().multiplyScalar((s + 1) / numberOfSegmentsSpanwise))
                .add(this.sweepVector.clone().multiplyScalar((s + 1) / numberOfSegmentsSpanwise));
            let elementInsideChord = (this.rootChord + (s / numberOfSegmentsSpanwise) * (tipChord - this.rootChord)) / numberOfSegmentsChordwise;
            let elementOutsideChord = (this.rootChord + ((s + 1) / numberOfSegmentsSpanwise) * (tipChord - this.rootChord)) / numberOfSegmentsChordwise;
            for(let c = 0; c < numberOfSegmentsChordwise; c++) {
                let elementInsideTip = stripInsideTip
                    .clone()
                    .add(this.rootVector.clone().normalize().multiplyScalar(elementInsideChord).multiplyScalar(c))
                    .add(this.thicknessVector.clone().multiplyScalar(-1.0 * thickness / 2.0));
                let elementInsideEnd = stripInsideTip
                    .clone()
                    .add(this.rootVector.clone().normalize().multiplyScalar(elementInsideChord).multiplyScalar(c + 1))
                    .add(this.thicknessVector.clone().multiplyScalar(-1.0 * thickness / 2.0));
                let elementOutsideTip = stripOutsideTip
                    .clone()
                    .add(this.rootVector.clone().normalize().multiplyScalar(elementOutsideChord).multiplyScalar(c))
                    .add(this.thicknessVector.clone().multiplyScalar(-1.0 * thickness / 2.0));
                let elementOutsideEnd = stripOutsideTip
                    .clone()
                    .add(this.rootVector.clone().normalize().multiplyScalar(elementOutsideChord).multiplyScalar(c + 1))
                    .add(this.thicknessVector.clone().multiplyScalar(-1.0 * thickness / 2.0));
                if(c == 0) {
                    elementInsideTip.sub(this.thicknessVector.clone().multiplyScalar(-1.0 * thickness / 2.0));
                    elementOutsideTip.sub(this.thicknessVector.clone().multiplyScalar(-1.0 * thickness / 2.0));
                }
                if(c == (numberOfSegmentsChordwise - 1)) {
                    elementInsideEnd.sub(this.thicknessVector.clone().multiplyScalar(-1.0 * thickness / 2.0));
                    elementOutsideEnd.sub(this.thicknessVector.clone().multiplyScalar(-1.0 * thickness / 2.0));
                }
                this.triangles.push(new Triangle(
                    elementInsideTip.toArray(),
                    elementOutsideEnd.toArray(),
                    elementInsideEnd.toArray()
                ));
                this.triangles.push(new Triangle(
                    elementInsideTip.toArray(),
                    elementOutsideTip.toArray(),
                    elementOutsideEnd.toArray()
                ));
            }
        }

        this.lines = this.triangles.map(t => t.lines);
        this.faces = this.triangles.map(t => t.face);
    }
}